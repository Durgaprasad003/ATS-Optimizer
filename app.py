
import os
import io
import base64
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import pdf2image
import google.generativeai as genai
from datetime import datetime
import pandas as pd
import re

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini model setup
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

def get_gemini_response(user_input, pdf_content, prompt):
    try:
        loader_placeholder = st.empty()

        loader_html = """
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    display: flex; align-items: center; justify-content: center;
                    background-color: rgba(255, 255, 255, 0.8); z-index: 9999;">
            <div style="text-align: center; display: flex; flex-direction: column; align-items: center;">
                <div style="border: 8px solid #f3f3f3;
                            border-top: 8px solid #3498db;
                            border-radius: 50%;
                            width: 60px;
                            height: 60px;
                            animation: spin 1s linear infinite;">
                </div>
                <p style="margin-top: 15px; font-weight: bold;">Processing with Gemini...</p>
            </div>
        </div>
        <style>
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        </style>
        """

        loader_placeholder.markdown(loader_html, unsafe_allow_html=True)

        response = model.generate_content(
            [user_input, pdf_content[0], prompt],
            generation_config={"max_output_tokens": 1024}
        )

        loader_placeholder.empty()
        return response.text

    except Exception as e:
        loader_placeholder.empty()
        return f"❌ Error: {e}"

def input_pdf_setup(uploaded_file):
    if uploaded_file and uploaded_file.name.endswith(".pdf"):
        try:
            images = pdf2image.convert_from_bytes(
                uploaded_file.read()
                # poppler_path=r"C:\\Users\\kella\\Downloads\\Release-24.08.0-0\\poppler-24.08.0\\Library\\bin"
            )
            first_page = images[0]
            img_byte_arr = io.BytesIO()
            first_page.save(img_byte_arr, format='JPEG')
            img_data = img_byte_arr.getvalue()
            pdf_parts = [{
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_data).decode('utf-8'),
            }]
            return pdf_parts
        except Exception as e:
            st.error(f"❌ PDF conversion failed: {e}")
            return None
    else:
        st.warning("📄 Please upload a valid PDF file.")
        return None

# ---- UI Setup ----
st.set_page_config(page_title="Gemini Resume Analyzer", page_icon=":robot_face:", layout="wide")

# Centered title and header using columns
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h1 style='text-align: center;'>🤖 Gemini Resume Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Your Smart ATS Resume Assistant</h4>", unsafe_allow_html=True)

# Expanded job role list
job_roles = [
    "Software Developer / Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer",
    "Data Analyst", "Data Scientist", "Machine Learning Engineer", "DevOps Engineer", "Cloud Engineer",
    "QA / Test Engineer", "Cybersecurity Analyst", "Database Administrator (DBA)",
    "Support Engineer / IT Support", "System Administrator", "Business Analyst",
    "Web Developer", "Mobile App Developer (Android/iOS)", "UI/UX Designer (technical + design)"
]

job_title = st.selectbox("🔍 Choose the Job Role you're applying for (optional):", ["None"] + job_roles)
if job_title == "None":
    job_title = "Technology Role"

input_text = st.text_area("📋 Paste Job Description:", placeholder="Paste the job description here")
uploaded_files = st.file_uploader("📤 Upload Resume PDFs", type=["pdf"], accept_multiple_files=True)
custom_question = st.text_input("❓ Ask your own question (optional)")

# Optimized Prompts
prompt_score = f"""
You are an advanced ATS (Applicant Tracking System) evaluator.
Analyze the uploaded resume in context of the job description for the role of {job_title}.
Return the following:
✅ Accurate Match Score (as a percentage)
📌 Key Missing Keywords (if any)
🎯 Predicted Hiring Potential (High / Medium / Low)
💡 Clear Suggestions to improve chances of shortlisting

List the missing keywords clearly under a heading called 'Missing Keywords:' (each on a new line).
"""

prompt_gap = f"""
You're a top-tier recruiter specializing in hiring for {job_title} roles.
Carefully compare the candidate's resume with the given job description.
Provide:
1. Skills or experiences that align well
2. Skills, tools, or technologies missing
3. Learning or improvement suggestions to make the candidate job-ready
"""

prompt_edit = f"""
Act as a resume optimization expert focused on {job_title} hiring.
Your job is to refine the content of the resume. Output:
- Rewritten bullet points with stronger action verbs
- Improved phrasing for clarity and impact
- Keyword-rich content (without repetition)
- Maintain original meaning but make it job-ready and ATS-optimized
"""

prompt_future_path = f"""
You're an AI Career Growth Strategist from the future.
Evaluate the resume and job description for the role of {job_title}.
Then return:
1. Two realistic next career roles the person can aim for
2. 5 Most important skills or certifications to acquire
3. Career path advice based on skill growth (not years)
4. Motivating and realistic roadmap tailored to the candidate's current profile
"""

history_data = []

if uploaded_files and input_text:
    for i, file in enumerate(uploaded_files):
        st.markdown(f"### 📄 Resume {i+1}: {file.name}")
        pdf_content = input_pdf_setup(file)
        if not pdf_content:
            continue

        response = get_gemini_response("", pdf_content, prompt_score + input_text)
        st.success(response)

        # Extract missing keywords more reliably
    
        score_line = response.splitlines()[0] if response else "N/A"
        history_data.append({"Resume": file.name, "Match Score": score_line, "Date": datetime.now().strftime("%Y-%m-%d %H:%M")})

        if st.checkbox(f"Show Skill Gap Analysis - {file.name}"):
            response = get_gemini_response("", pdf_content, prompt_gap + input_text)
            st.info(response)

        if custom_question:
            response = get_gemini_response(custom_question, pdf_content, input_text)
            st.write("🧠 Gemini Answer:", response)

        if st.checkbox(f"Suggest Resume Improvements - {file.name}"):
            response = get_gemini_response("", pdf_content, prompt_edit + input_text)
            st.warning(response)

        if st.checkbox(f"🔮 Predict Career Trajectory (Innovative) - {file.name}"):
            response = get_gemini_response("", pdf_content, prompt_future_path)
            st.info(response)

    if history_data:
        st.markdown("### 📊 Resume Score History")
        df = pd.DataFrame(history_data)
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download History CSV", csv, file_name="resume_score_history.csv")

else:
    st.info("Please upload at least one resume and provide the job description.")
