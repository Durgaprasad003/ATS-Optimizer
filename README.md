# ATS-Optimizer

A smart, AI-powered Streamlit web application that evaluates resumes against job descriptions using Google's Gemini Pro API. The tool provides ATS match scores, missing keyword suggestions, resume optimization tips, career predictions, and a skill gap analysis

# 🚀 Features

🤖 AI-Powered Resume Analysis using Gemini Pro

✅ ATS-style Match Score for each resume

📌 Missing Keywords from job description

🛠 Resume Optimization suggestions

🔍 Skill Gap Analysis

🔮 Future Career Path Predictions

📂 Score History & CSV Export

🔄 Analyze Multiple Resumes at once

📋 Custom questions to ask Gemini


# 🛠 Tech Stack

Streamlit

Python

Google Generative AI (Gemini API)

pdf2image

Pillow

dotenv


# 🔧 Installation

Clone the repo'
git clone https://github.com/yourusername/gemini-resume-analyzer.git
cd gemini-resume-analyzer
Install dependencies
pip install -r requirements.txt
Setup your Gemini API key

Create a .env file:
GOOGLE_API_KEY=your-gemini-api-key
[Only for Windows Users] Install Poppler

Download Poppler for Windows: https://github.com/oschwartz10612/poppler-windows/releases/

Unzip and place it somewhere (e.g., C:\poppler)

In the code, set:
poppler_path=r"C:\\poppler\\poppler-24.08.0\\Library\\bin"


#Run the App
streamlit run app.py

# 🌟 Show Some Love

Star this repo if you found it helpful!

Made with ❤️ using Streamlit & Gemini API























