# 🧠 HYRNN – AI-Powered Resume Screening Tool

### Intelligent Recruitment & Candidate Ranking Platform

**Developed by: CHAND KUJRA**

HYRNN is an AI-assisted resume screening platform built using Python and Streamlit. It analyzes candidate resumes against job descriptions, identifies relevant skills, calculates text similarity scores, ranks candidates and generates downloadable screening reports.

---

## 🚀 Project Overview

Recruiters often receive hundreds of resumes for a single job opening. Manually reviewing every resume takes time and effort.

HYRNN helps simplify this process by extracting resume content, comparing candidate skills with job requirements and generating a candidate ranking report.

## ✨ Key Features

- 📄 **Multiple Resume Upload:** Upload multiple PDF, DOCX and TXT resumes.
- 📋 **Job Description Analysis:** Upload or paste job descriptions.
- 🤖 **AI-Assisted Matching:** TF-IDF and cosine similarity-based text matching.
- 🎯 **Skill Matching:** Identify matched and missing technical skills.
- 🏆 **Candidate Ranking:** Rank candidates according to their match scores.
- 📊 **Analytics Dashboard:** Visualize candidate matching results.
- 📥 **CSV Report Export:** Download screening results.
- ⚙️ **Configurable Threshold:** Set a shortlist-for-review score.
- 🔌 **FastAPI Support:** Optional resume-matching API.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Streamlit | Interactive dashboard |
| Pandas | Data processing |
| Scikit-learn | Text similarity and matching |
| PDFPlumber | PDF text extraction |
| python-docx | Word document extraction |
| Plotly | Analytics and charts |
| FastAPI | REST API |
| Pytest | Testing |

## 📁 Project Structure

```text
HYRNN-Resume-Screening-Tool/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── api/
│   ├── __init__.py
│   └── main.py
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── parser.py
│   ├── matcher.py
│   └── report.py
│
├── data/
│   └── job_description.txt
│
├── resumes/
│
├── outputs/
│
├── docs/
│   └── PROJECT_OVERVIEW.md
│
└── tests/
    └── test_matcher.py
```

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/erchandkujra-ai/HYRNN-Resume-Screening-Tool.git
```

### 2. Open Project Folder

```bash
cd HYRNN-Resume-Screening-Tool
```

### 3. Create Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate Virtual Environment (Windows)

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Run Streamlit Application

```bash
python -m streamlit run app.py --server.port 8506
```

Open in browser:

```text
http://localhost:8506
```

## 🔌 Run FastAPI Backend

Start the API:

```bash
uvicorn api.main:app --reload --port 8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## 🧪 Run Tests

```bash
python -m pytest -q
```

## 📊 How It Works

1. Recruiter enters or uploads a job description.
2. Recruiter uploads candidate resumes.
3. The parser extracts text from supported documents.
4. The matching engine calculates text similarity.
5. The skill matcher identifies matching and missing skills.
6. Candidates are ranked by their overall match score.
7. Recruiter downloads the screening report.

## 📈 Matching Methodology

HYRNN uses two matching signals:

- **Text Similarity:** TF-IDF with cosine similarity.
- **Skill Matching:** Compares detected skills in the job description and resume.

When job-description skills are detected, the overall score is calculated as:

```text
Overall Match =
(55% × Text Similarity) +
(45% × Skill Match)
```

The shortlist threshold is configurable by the recruiter.

## 🔮 Future Enhancements

- NLP-based resume understanding.
- Named Entity Recognition for candidate information.
- OCR support for scanned PDF resumes.
- Database integration.
- Recruiter authentication and role management.
- Email notifications for shortlisted candidates.
- Advanced candidate comparison.
- Cloud deployment.

## ⚠️ Important Disclaimer

HYRNN is an educational and portfolio project. Its match scores are approximate text-similarity indicators, not validated predictions of job performance.

Automated scores should not be the sole basis for hiring decisions. Recruiters must review candidates fairly using relevant job-related criteria.

## 👨‍💻 Developer

**CHAND KUJRA**

B.Tech – Computer Science and Engineering (CSE)  
IET Bhaddal Technical Campus, Ropar, Punjab  
Currently studying: 3rd Semester

GitHub: https://github.com/erchandkujra-ai

---

⭐ If you find this project useful, consider giving the repository a star!

**HYRNN – Making Recruitment Smarter with AI-Assisted Technology.**