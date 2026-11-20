
import re


SKILLS_DATABASE = [
    "Python",
    "Java",
    "C++",
    "C",
    "JavaScript",
    "HTML",
    "CSS",
    "React",
    "Node.js",
    "Flask",
    "Django",
    "FastAPI",
    "SQL",
    "MySQL",
    "MongoDB",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Scikit-learn",
    "Machine Learning",
    "Deep Learning",
    "Data Analysis",
    "Data Science",
    "Statistics",
    "Git",
    "GitHub",
    "REST API",
    "Power BI",
    "Excel",
    "TensorFlow",
    "PyTorch",
    "AWS",
    "Docker",
    "Linux"
]


def extract_skills(text):
    """
    Identify technical skills from text.
    """

    found_skills = []
    text_lower = text.lower()

    for skill in SKILLS_DATABASE:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return sorted(set(found_skills))


def calculate_skill_match(resume_skills, required_skills):
    """
    Calculate percentage of required skills matched.
    """

    if not required_skills:
        return 0.0

    matched = set(resume_skills) & set(required_skills)

    return round(
        (len(matched) / len(set(required_skills))) * 100,
        2
    )
