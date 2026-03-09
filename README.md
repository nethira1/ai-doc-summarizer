# 📄 AI Document Summarizer (FREE - Powered by Google Gemini)

Summarize PDFs and text files using Google Gemini AI — completely free, no credit card needed!

## ✨ Features
- Upload PDF or TXT files
- Instant AI summary (3-5 sentences)
- Extract top 5 key points
- Ask questions about your document (Q&A chat)

## 🚀 Setup (3 Steps)

### Step 1 — Get your FREE Gemini API Key
1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (starts with `AIza...`)

### Step 2 — Install dependencies
Open terminal in this folder and run:
```bash
pip install -r requirements.txt
```

### Step 3 — Run the app
```bash
streamlit run app.py
```
Opens at: http://localhost:8501

Paste your Gemini API key in the sidebar — done! 🎉

## ☁️ Deploy Free on Render.com
1. Push folder to GitHub
2. Go to render.com → New Web Service
3. Connect your repo
4. Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. Add environment variable: `GEMINI_API_KEY=your_key_here`

## 📁 Project Structure
```
ai-doc-summarizer/
├── app.py            ← Main application (Gemini powered)
├── requirements.txt  ← Python dependencies
└── README.md         ← This file
```
