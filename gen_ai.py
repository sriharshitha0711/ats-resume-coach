from groq import Groq
import os

# --------------------------------------------------
# GROQ CLIENT (FREE)
# --------------------------------------------------
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY not found. Set it using:\n"
        "setx GROQ_API_KEY \"your_groq_key_here\""
    )

client = Groq(api_key=API_KEY)

# --------------------------------------------------
# 1. GEN-AI SUGGESTIONS (ATS IMPROVEMENTS)
# --------------------------------------------------
def gen_ai_suggestions(missing_skills):
    if not missing_skills:
        return "Your resume already aligns well with the job description."

    prompt = f"""
You are an ATS resume expert.

The candidate is missing these skills:
{", ".join(missing_skills)}

Provide:
- Clear resume improvement suggestions
- ATS-friendly bullet points
- How to naturally add these skills
Keep it concise.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content


# --------------------------------------------------
# 2. AI RESUME GENERATOR
# --------------------------------------------------
def generate_resume(user_profile, target_role):
    prompt = f"""
Create an ATS-optimized resume.

Target Role: {target_role}

Candidate Details:
Name: {user_profile.get("name", "Candidate")}
Education: {user_profile.get("education", "Not provided")}
Skills: {user_profile.get("skills", "Not provided")}
Projects: {user_profile.get("projects", "Not provided")}
Experience: {user_profile.get("experience", "Fresher")}

Use strong action verbs and ATS keywords.
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content


# --------------------------------------------------
# 3. INTERVIEW QUESTION GENERATOR
# --------------------------------------------------
def generate_interview_questions(resume_text, job_role):
    prompt = f"""
Resume:
{resume_text}

Job Role:
{job_role}

Generate:
- 3 technical questions
- 2 HR questions
- 2 behavioral questions
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    return response.choices[0].message.content


# --------------------------------------------------
# 4. INTERVIEW ANSWER EVALUATION
# --------------------------------------------------
def evaluate_answer(question, answer):
    prompt = f"""
Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate and provide:
- Score out of 10
- Strengths
- Areas for improvement
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content
