import pandas as pd
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def analyze_resume(resume_text):

    # -------- FIXED DATASET PATH (important) --------
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "dataset", "job_roles.csv")

    jobs = pd.read_csv(DATA_PATH)

    resume_text = resume_text.lower()

    # -------- SKILL EXTRACTION --------
    all_skills = set()
    for skill_list in jobs['skills']:
        for skill in skill_list.split():
            all_skills.add(skill.lower())

    found_skills = []
    for skill in all_skills:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, resume_text):
            found_skills.append(skill)

    # -------- CAREER PREDICTION (TF-IDF + Cosine Similarity) --------
    job_skill_texts = jobs['skills'].tolist()
    user_skill_text = " ".join(found_skills)
    job_skill_texts.append(user_skill_text)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(job_skill_texts)

    similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    best_match_index = similarities.argmax()
    best_role = jobs.iloc[best_match_index]['role']
    confidence = float(similarities[0][best_match_index] * 100)

    # -------- SKILL GAP ANALYSIS --------
    required_skills = jobs.iloc[best_match_index]['skills'].split()
    missing_skills = [skill for skill in required_skills if skill not in found_skills]

    # -------- CAREER ROADMAP --------
    career_paths = {
        "Data Scientist": [
            "Learn NumPy & Pandas deeply",
            "Study Machine Learning algorithms",
            "Build ML projects",
            "Apply internships"
        ],
        "Data Analyst": [
            "Learn SQL",
            "Master Excel",
            "Learn Power BI or Tableau",
            "Build dashboard projects",
            "Apply analyst internships"
        ],
        "Web Developer": [
            "Learn HTML, CSS, JavaScript properly",
            "Learn React",
            "Build responsive websites",
            "Learn backend basics",
            "Apply for internships"
        ]
    }

    roadmap = career_paths.get(
        best_role,
        ["Learn required skills", "Build projects", "Apply internships"]
    )

    # -------- FINAL OUTPUT --------
    return {
        "role": best_role,
        "confidence": round(confidence, 2),
        "detected_skills": found_skills,
        "missing_skills": missing_skills,
        "roadmap": roadmap
    }
