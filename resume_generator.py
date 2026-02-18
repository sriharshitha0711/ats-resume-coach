# resume_generator.py

import streamlit as st
import pdfkit
config = pdfkit.configuration(
    wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
)

# ----------------------
# Page config
# ----------------------
st.set_page_config(page_title="Resume Generator", layout="centered")
st.title("📝 Resume Generator")
st.write("Fill details, choose a template, preview, and download your resume.")

# ----------------------
# Template mapping
# ----------------------
TEMPLATES = {
    "Classic Blue": ("templates/template1.html", "previews/template1.png"),
    "Modern Black": ("templates/template2.html", "previews/template2.png"),
    "Creative": ("templates/template3.html", "previews/template3.png"),
    "Minimal ATS": ("templates/template4.html", "previews/template4.png"),
    "Tech": ("templates/template5.html", "previews/template5.png"),
}

# ----------------------
# Template selection + preview
# ----------------------
choice = st.selectbox("Choose Resume Template", TEMPLATES.keys())

html_file, preview_img = TEMPLATES[choice]

st.image(preview_img, caption="Template Preview", use_container_width=True)

# ----------------------
# User input form
# ----------------------
with st.form("resume_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    education = st.text_area("Education")
    skills = st.text_area("Skills")
    experience = st.text_area("Experience")
    projects = st.text_area("Projects")

    submitted = st.form_submit_button("Generate Resume")

# ----------------------
# Generate PDF
# ----------------------
if submitted:
    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace("{{name}}", name)
    html = html.replace("{{email}}", email)
    html = html.replace("{{phone}}", phone)
    html = html.replace("{{education}}", education)
    html = html.replace("{{skills}}", skills)
    html = html.replace("{{experience}}", experience)
    html = html.replace("{{projects}}", projects)

    pdfkit.from_string(html, "resume.pdf", configuration=config)



    with open("resume.pdf", "rb") as f:
        st.download_button(
            "⬇️ Download Resume PDF",
            f,
            file_name="resume.pdf",
            mime="application/pdf"
        )
st.markdown("## 🎤 Interview Coach")

# ----------------------
# Role & Level Selection
# ----------------------
role = st.selectbox(
    "Choose Job Role",
    ["Software Engineer", "Data Analyst", "AI/ML Engineer", "Frontend Developer", "Backend Developer"]
)

level = st.selectbox(
    "Interview Level",
    ["Beginner", "Intermediate", "Advanced"]
)

# ----------------------
# Question Bank
# ----------------------
QUESTIONS = {
    "Software Engineer": {
        "Beginner": "What is Object-Oriented Programming?",
        "Intermediate": "Explain difference between abstract class and interface.",
        "Advanced": "How does garbage collection work in Java?"
    },
    "Data Analyst": {
        "Beginner": "What is data cleaning?",
        "Intermediate": "Explain normalization and denormalization.",
        "Advanced": "How would you handle missing data in a large dataset?"
    },
    "AI/ML Engineer": {
        "Beginner": "What is Machine Learning?",
        "Intermediate": "Explain overfitting and how to prevent it.",
        "Advanced": "How does gradient descent work mathematically?"
    },
    "Frontend Developer": {
        "Beginner": "What is HTML and CSS?",
        "Intermediate": "Explain React state and props.",
        "Advanced": "How does Virtual DOM improve performance?"
    },
    "Backend Developer": {
        "Beginner": "What is an API?",
        "Intermediate": "Explain REST vs SOAP.",
        "Advanced": "How do you design a scalable backend system?"
    }
}

question = QUESTIONS[role][level]

# ----------------------
# Display Question
# ----------------------
st.subheader("📌 Interview Question")
st.info(question)

# ----------------------
# Answer Input
# ----------------------
answer = st.text_area(
    "✍️ Your Answer",
    height=200,
    placeholder="Type your answer here..."
)

# ----------------------
# Feedback Button
# ----------------------
if st.button("Get Feedback"):
    if len(answer.strip()) < 20:
        st.warning("⚠️ Answer is too short. Please write a more detailed answer.")
    else:
        # Temporary rule-based feedback (AI can replace this)
        st.subheader("🧠 Feedback")

        st.success("✅ Good effort! Your answer covers the basics.")

        st.markdown("**Strengths:**")
        st.write("- Clear explanation")
        st.write("- Relevant to the question")

        st.markdown("**Improvements:**")
        st.write("- Add real-world examples")
        st.write("- Use technical terminology more precisely")

        st.markdown("**Score:** ⭐⭐⭐⭐☆ (4/5)")
st.markdown("---")
st.subheader("📝 User Feedback")

rating = st.radio(
    "How helpful was this resume generator?",
    [1, 2, 3, 4, 5],
    horizontal=True
)

comment = st.text_area(
    "Any suggestions or issues? (optional)",
    placeholder="Your feedback helps us improve..."
)

if st.button("Submit Feedback"):
    import csv
    from datetime import datetime

    with open("feedback.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            rating,
            comment
        ])

    st.success("✅ Thank you for your feedback!")

