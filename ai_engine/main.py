import pandas as pd
import re

# ---------------- LOAD DATASET ----------------
jobs = pd.read_csv("dataset/job_roles.csv")

print("\n=== JOB DATASET ===")
print(jobs.head())

# ---------------- LOAD RESUME ----------------
with open("resumes/resume1.txt", "r", encoding="utf-8") as f:
    resume_text = f.read().lower()

print("\n=== RESUME TEXT ===")
print(resume_text)

# ---------------- SKILL VOCABULARY ----------------
# collect all skills from dataset
all_skills = set()

for skill_list in jobs['skills']:
    for skill in skill_list.split():
        all_skills.add(skill.lower())

# ---------------- EXTRACT SKILLS FROM RESUME ----------------
found_skills = []

for skill in all_skills:
    pattern = r'\b' + re.escape(skill) + r'\b'
    if re.search(pattern, resume_text):
        found_skills.append(skill)

print("\n=== EXTRACTED SKILLS ===")
print(found_skills)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- PREPARE DATA FOR MODEL ----------------

# combine all job skill texts
job_skill_texts = jobs['skills'].tolist()

# add user skills as last entry
user_skill_text = " ".join(found_skills)
job_skill_texts.append(user_skill_text)

# convert text → numbers
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(job_skill_texts)

# last row is user
similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

# get best match
best_match_index = similarities.argmax()
best_role = jobs.iloc[best_match_index]['role']
confidence = similarities[0][best_match_index] * 100

print("\n=== PREDICTED CAREER ROLE ===")
print("Role:", best_role)
print("Match Score: {:.2f}%".format(confidence))
# ---------------- SKILL GAP ANALYSIS ----------------

required_skills = jobs.iloc[best_match_index]['skills'].split()

missing_skills = []
for skill in required_skills:
    if skill not in found_skills:
        missing_skills.append(skill)

print("\n=== SKILL GAP ANALYSIS ===")
print("You need to learn:")
for skill in missing_skills:
    print("-", skill)
# ---------------- CAREER PATH RECOMMENDATION ----------------

career_paths = {
    "Data Scientist": [
        "Learn NumPy & Pandas deeply",
        "Study Machine Learning algorithms (scikit-learn)",
        "Learn data visualization",
        "Build ML projects",
        "Apply for internships"
    ],
    "Data Analyst": [
        "Learn SQL",
        "Master Excel",
        "Learn Power BI or Tableau",
        "Do dashboard projects",
        "Apply for analyst internships"
    ],
    "Web Developer": [
        "Learn HTML, CSS, JavaScript properly",
        "Learn React",
        "Build responsive websites",
        "Learn backend basics",
        "Apply for web internships"
    ]
}

print("\n=== CAREER ROADMAP ===")

if best_role in career_paths:
    for step in career_paths[best_role]:
        print("->", step)
else:
    print("General path: Learn core skills, build projects, apply internships")
from model.predictor import analyze_resume

with open("resumes/resume1.txt", "r", encoding="utf-8") as f:
    text = f.read()

result = analyze_resume(text)
print(result)

