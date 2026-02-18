import tempfile

from resume_parser import extract_resume_text, clean_text
from jd_parser import extract_jd_text
from ats_scorer import calculate_ats_score
from section_scorer import section_match_score
from gen_ai import gen_ai_suggestions
from skill_utils import clean_skill_list
from skill_extractor import extract_skills


def run_ats_analysis(resume_file, jd_file):
    # ---- Save uploaded files temporarily ----
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_resume:
        temp_resume.write(resume_file.read())
        resume_path = temp_resume.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_jd:
        temp_jd.write(jd_file.read())
        jd_path = temp_jd.name

    # ---- Extract & clean text ----
    raw_resume = extract_resume_text(resume_path)
    raw_jd = extract_jd_text(jd_path)

    clean_resume = clean_text(raw_resume)
    clean_jd = clean_text(raw_jd)

    # ---- ATS score ----
    ats_score = calculate_ats_score(clean_resume, clean_jd)

    # ---- Skill Extraction (IMPORTANT FIX) ----
    resume_skills = extract_skills(clean_resume)
    jd_skills = extract_skills(clean_jd)

    matched_skills = clean_skill_list(resume_skills & jd_skills)
    missing_skills = clean_skill_list(jd_skills - resume_skills)

    # ---- Section-wise scoring (UNCHANGED) ----
    skills_kw = {"skills", "python", "sql", "data", "machine", "learning"}
    projects_kw = {"project", "projects", "developed", "built"}
    experience_kw = {"experience", "internship", "worked"}
    education_kw = {"education", "degree", "university"}

    section_scores = {
        "Skills": section_match_score(clean_resume, clean_jd, skills_kw),
        "Projects": section_match_score(clean_resume, clean_jd, projects_kw),
        "Experience": section_match_score(clean_resume, clean_jd, experience_kw),
        "Education": section_match_score(clean_resume, clean_jd, education_kw),
    }

    # ---- Gen-AI Suggestions ----
    ai_suggestions = (
        gen_ai_suggestions(missing_skills)
        if missing_skills
        else "Great match! No improvements needed."
    )

    return {
        "ats_score": ats_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "section_scores": section_scores,
        "ai_suggestions": ai_suggestions,
    }


# ================== NEW FEATURES ADDED ==================

from resume_generator import build_resume
from interview_engine import start_interview, assess_answer


def run_full_resume_pipeline(user_profile, job_description, target_role):
    """
    AI Resume Generation + ATS Analysis + Suggestions
    """

    # ---- Step 1: Generate Resume ----
    generated_resume = build_resume(user_profile, target_role)

    # ---- Step 2: Clean inputs ----
    clean_resume = clean_text(generated_resume)
    clean_jd = clean_text(job_description)

    # ---- Step 3: ATS Scoring ----
    ats_score = calculate_ats_score(clean_resume, clean_jd)

    # ---- Skill-based comparison (FIXED) ----
    resume_skills = extract_skills(clean_resume)
    jd_skills = extract_skills(clean_jd)

    matched_skills = clean_skill_list(resume_skills & jd_skills)
    missing_skills = clean_skill_list(jd_skills - resume_skills)

    # ---- Step 4: AI Suggestions ----
    ai_suggestions = (
        gen_ai_suggestions(missing_skills)
        if missing_skills
        else "Excellent match! Resume is well aligned with the job description."
    )

    return {
        "generated_resume": generated_resume,
        "ats_score": ats_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "ai_suggestions": ai_suggestions,
    }


def run_interview_session(resume_text, job_role):
    """
    Generate AI interview questions
    """
    return start_interview(resume_text, job_role)


def evaluate_interview_answer(question, user_answer):
    """
    Evaluate interview answer using AI
    """
    return assess_answer(question, user_answer)
