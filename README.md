# resume-screening-tool
## AI Powered Resume Screening Tool

This repository contains a Streamlit web app that uses NLP and sentence embeddings to extract and rank candidate resumes based on job descriptions.

## Features:
- Extracts text from PDF, DOCX, and TXT resumes
- Parses key sections (skills, education, experience) using spaCy and transformer-based classifiers
- Extracts organizations and job titles using Named Entity Recognition (NER)
- Fine-tuned section extraction using rules and learned models
- Computes cosine similarity between candidate profiles and job descriptions using SBERT
- Clusters similar resumes using KMeans
- Ranks candidates and displays extracted info in an interactive dashboard
  
## Repository Structure
```
resume-screening-tool/
├── app.py                   # Main Streamlit application
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container configuration
├── render.yaml              # Render deployment configuration
├── .gitignore               # Files to ignore in version control
├── .github/
│   └── workflows/
│       └── docker-deploy.yml  # GitHub Actions for Docker deployment
├── README.md                # Project overview and instructions
└── sample_resumes/          # Folder for sample PDF resumes
```

---

