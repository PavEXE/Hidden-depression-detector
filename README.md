# 🧠 Hidden Depression Detection Through Social Media Behavior

> **Resonate 2026 Hackathon · ByteForce4 · Track 1**

## Problem Statement

Depression is often called the "invisible illness." Millions of people show signs of depression through their social media posts — changes in language, increased self-referential writing, expressions of hopelessness — long before they seek professional help. Traditional detection methods require clinical intervention, but social media provides an earlier, passive signal.

**The problem:** There is no accessible, real-time tool that can flag potential depression signals in social media posts and suggest timely mental health resources.

## Our Solution

A web-based AI-powered tool that analyzes the text of social media posts and detects hidden depression signals using:
- **NLP feature extraction** — keyword lexicons, linguistic patterns, self-referential language
- **Risk scoring engine** — weighted multi-factor scoring with crisis language detection
- **Platform-aware analysis** — tuned for Twitter, Reddit, Instagram, Facebook
- **Actionable output** — risk level, detected signals, and crisis resources

## Demo

Live Demo: *(add your deployed link here after deployment)*

## Features

- 🔍 Single post analysis with detailed breakdown
- 📊 Batch analysis for multiple posts at once
- 🚨 Crisis language detection with immediate helpline resources
- 📱 Platform-aware scoring (Twitter, Reddit, Instagram, Facebook)
- 🎯 Detected signals explanation (not a black box)

## Tech Stack

- **Backend:** Python, Flask
- **NLP:** Rule-based lexicon + linguistic feature extraction
- **Frontend:** HTML, CSS, Vanilla JS
- **Deployment:** Render / Railway (Gunicorn)

## How to Run Locally

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd depression-detection

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py

# 4. Open in browser
# http://localhost:5000
```

## Project Structure

```
depression-detection/
├── app.py                  # Flask application entry point
├── requirements.txt        # Python dependencies
├── Procfile                # Deployment config
├── src/
│   ├── analyzer.py         # Risk scoring engine
│   └── feature_extractor.py# NLP feature extraction
└── templates/
    └── index.html          # Frontend UI
```

## How It Works

1. User pastes a social media post
2. `feature_extractor.py` scans for:
   - Depression, anxiety, isolation, and self-harm keywords
   - Linguistic markers: negation, ellipsis, caps ratio, first-person ratio
   - Positive language (reduces score)
3. `analyzer.py` computes a weighted risk score (0–1)
4. Crisis phrases trigger a mandatory high-risk flag
5. Result shown with explanation + mental health resources

## Mental Health Resources

- **iCall (India):** 9152987821
- **Vandrevala Foundation (24/7):** 1860-2662-345
- **International Crisis Centers:** https://www.iasp.info/resources/Crisis_Centres/

---

> ⚠️ **Disclaimer:** This tool is for research and awareness purposes only. It is not a clinical diagnostic tool. Always consult a qualified mental health professional.
