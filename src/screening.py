
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.extractor import extract_text
from src.skills import extract_skills, calculate_skill_match


def screen_resumes(resume_paths, job_description, threshold=50):
    """
    Compare resumes with a job description
    and return ranked candidate results.
    """

    job_skills = extract_skills(job_description)

    results = []

    for resume_path in resume_paths:

        try:
            resume_text = extract_text(resume_path)

            if not resume_text.strip():
                continue

            resume_skills = extract_skills(resume_text)

            vectorizer = TfidfVectorizer(
                stop_words="english",
                ngram_range=(1, 2)
            )

            vectors = vectorizer.fit_transform(
                [job_description, resume_text]
            )

            similarity = cosine_similarity(
                vectors[0:1],
                vectors[1:2]
            )[0][0] * 100

            skill_match = calculate_skill_match(
                resume_skills,
                job_skills
            )

            final_score = (
                0.60 * similarity
                + 0.40 * skill_match
            )

            matched_skills = sorted(
                set(resume_skills) & set(job_skills)
            )

            missing_skills = sorted(
                set(job_skills) - set(resume_skills)
            )

            status = (
                "Shortlisted for Review"
                if final_score >= threshold
                else "Needs Manual Review"
            )

            results.append({
                "candidate": Path(resume_path).stem,
                "resume_file": Path(resume_path).name,
                "similarity_score": round(similarity, 2),
                "skill_match": skill_match,
                "final_score": round(final_score, 2),
                "matched_skills": ", ".join(matched_skills),
                "missing_skills": ", ".join(missing_skills),
                "status": status
            })

        except Exception as error:
            results.append({
                "candidate": Path(resume_path).stem,
                "resume_file": Path(resume_path).name,
                "similarity_score": 0,
                "skill_match": 0,
                "final_score": 0,
                "matched_skills": "",
                "missing_skills": "",
                "status": f"Processing Error: {error}"
            })

    results.sort(
        key=lambda item: item["final_score"],
        reverse=True
    )

    return results
