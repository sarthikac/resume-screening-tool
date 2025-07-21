import fitz  # PyMuPDF
import spacy
import os
import docx
import streamlit as st
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer, util
from io import StringIO

# Load NLP models
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")

SUPPORTED_TYPES = ("pdf", "docx", "txt")

def extract_text(file):
    file_type = file.name.split(".")[-1].lower()
    if file_type == "pdf":
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return " ".join([page.get_text() for page in doc])
    elif file_type == "docx":
        doc = docx.Document(file)
        return " ".join([para.text for para in doc.paragraphs])
    elif file_type == "txt":
        return StringIO(file.getvalue().decode("utf-8")).read()
    else:
        return ""

def extract_sections(text):
    section_headers = ["skills", "education", "experience"]
    sections = {key: "" for key in section_headers}
    lower_text = text.lower()
    for section in section_headers:
        idx = lower_text.find(section)
        if idx != -1:
            next_indices = [lower_text.find(h, idx + 1) for h in section_headers if lower_text.find(h, idx + 1) != -1]
            end_idx = min(next_indices) if next_indices else len(text)
            sections[section] = text[idx:end_idx]
    return sections

def extract_entities(text):
    doc = nlp(text)
    orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    titles = [ent.text for ent in doc.ents if ent.label_ == "JOB_TITLE"] if "JOB_TITLE" in nlp.get_pipe("ner").labels else []
    return orgs, titles

def embed_and_score(candidate_text, job_description):
    candidate_emb = model.encode(candidate_text, convert_to_tensor=True)
    job_emb = model.encode(job_description, convert_to_tensor=True)
    return util.pytorch_cos_sim(candidate_emb, job_emb).item(), candidate_emb

def process_resume(file, job_description):
    text = extract_text(file)
    sections = extract_sections(text)
    orgs, titles = extract_entities(text)
    combined = " ".join(sections.values())
    score, embedding = embed_and_score(combined, job_description)
    sections["organizations"] = ", ".join(set(orgs))
    sections["titles"] = ", ".join(set(titles))
    return score, sections, embedding

# Streamlit UI
st.title("AI-Powered Resume Screening Tool")
job_desc = st.text_area("Enter Job Description:")
uploaded_files = st.file_uploader("Upload Resumes (PDF, DOCX, TXT)", type=SUPPORTED_TYPES, accept_multiple_files=True)

if uploaded_files and job_desc:
    results = []
    embeddings = []
    for file in uploaded_files:
        score, sections, emb = process_resume(file, job_desc)
        embeddings.append(emb.cpu().numpy())
        results.append((file.name, score, sections))

    kmeans = KMeans(n_clusters=min(3, len(embeddings)), random_state=42).fit(embeddings)
    labels = kmeans.labels_

    results = list(zip(results, labels))
    results.sort(key=lambda x: x[0][1], reverse=True)

    st.subheader("Ranked Candidates")
    for (name, score, sections), cluster in results:
        st.markdown(f"**{name}** - Score: {score:.2f} | Cluster: {cluster}")
        with st.expander("View Extracted Info"):
            st.write("**Skills**", sections['skills'])
            st.write("**Education**", sections['education'])
            st.write("**Experience**", sections['experience'])
            st.write("**Organizations Mentioned**", sections.get('organizations', 'N/A'))
            st.write("**Job Titles Mentioned**", sections.get('titles', 'N/A'))





