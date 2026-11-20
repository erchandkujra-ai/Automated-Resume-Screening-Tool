
from pathlib import Path
import pandas as pd

from src.screening import screen_resumes


BASE_DIR = Path(__file__).resolve().parent

RESUME_DIR = BASE_DIR / "resumes"
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

JOB_FILE = DATA_DIR / "job_description.txt"


def main():

    OUTPUT_DIR.mkdir(exist_ok=True)

    if not JOB_FILE.exists():
        print("Job description file not found!")
        return

    job_description = JOB_FILE.read_text(
        encoding="utf-8"
    )

    resume_paths = [
        path
        for path in RESUME_DIR.iterdir()
        if path.is_file()
        and path.suffix.lower() in [".pdf", ".docx", ".txt"]
    ]

    if not resume_paths:
        print("No resumes found in resumes folder!")
        return

    print("\nStarting Resume Screening...\n")

    results = screen_resumes(
        resume_paths,
        job_description
    )

    dataframe = pd.DataFrame(results)

    report_path = OUTPUT_DIR / "ranking_report.csv"

    dataframe.to_csv(
        report_path,
        index=False
    )

    print(dataframe.to_string(index=False))

    print("\nScreening completed!")
    print(f"Report saved at: {report_path}")


if __name__ == "__main__":
    main()
