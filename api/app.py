
from pathlib import Path
import shutil
import uuid

import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from src.screening import screen_resumes


# -------------------------------------------------
# PROJECT PATHS
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
JOB_FILE = BASE_DIR / "data" / "job_description.txt"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------
# FASTAPI APPLICATION
# -------------------------------------------------

app = FastAPI(
    title="Automated Resume Screening Tool",
    description="AI-based resume screening and ranking API",
    version="1.0.0"
)


# -------------------------------------------------
# HOME ROUTE
# -------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to Automated Resume Screening Tool",
        "status": "API is running",
        "documentation": "/docs"
    }


# -------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# -------------------------------------------------
# RESUME SCREENING API
# -------------------------------------------------

@app.post("/screen")
async def screen_candidates(
    files: list[UploadFile] = File(...)
):
    allowed_extensions = {
        ".pdf",
        ".docx",
        ".txt"
    }

    if not files:
        raise HTTPException(
            status_code=400,
            detail="Please upload at least one resume."
        )

    if not JOB_FILE.exists():
        raise HTTPException(
            status_code=404,
            detail="Job description file not found."
        )

    job_description = JOB_FILE.read_text(
        encoding="utf-8"
    )

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description is empty."
        )

    request_id = uuid.uuid4().hex

    request_dir = UPLOAD_DIR / request_id
    request_dir.mkdir(parents=True, exist_ok=True)

    saved_files = []

    try:
        for file in files:

            extension = Path(file.filename or "").suffix.lower()

            if extension not in allowed_extensions:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file format: {extension}"
                )

            if not file.filename:
                raise HTTPException(
                    status_code=400,
                    detail="Uploaded file has no filename."
                )

            safe_filename = (
                f"{uuid.uuid4().hex}{extension}"
            )

            file_path = request_dir / safe_filename

            with file_path.open("wb") as buffer:
                shutil.copyfileobj(
                    file.file,
                    buffer
                )

            saved_files.append(file_path)

        # Run resume screening
        results = screen_resumes(
            saved_files,
            job_description
        )

        if not results:
            raise HTTPException(
                status_code=400,
                detail="No readable resumes were found."
            )

        # Create CSV report
        report_path = (
            OUTPUT_DIR / f"ranking_report_{request_id}.csv"
        )

        dataframe = pd.DataFrame(results)

        dataframe.to_csv(
            report_path,
            index=False
        )

        return {
            "message": "Resume screening completed successfully.",
            "total_resumes": len(saved_files),
            "total_processed": len(results),
            "results": results,
            "download_url": f"/download/{report_path.name}",
            "notice": (
                "Scores are decision-support information only. "
                "A human recruiter must review every candidate."
            )
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Screening failed: {str(error)}"
        )

    finally:
        for file in files:
            await file.close()


# -------------------------------------------------
# DOWNLOAD CSV REPORT
# -------------------------------------------------

@app.get("/download/{filename}")
def download_report(filename: str):

    # Prevent directory traversal
    if Path(filename).name != filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename."
        )

    report_path = OUTPUT_DIR / filename

    if not report_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Report not found."
        )

    return FileResponse(
        path=report_path,
        filename=filename,
        media_type="text/csv"
    )
