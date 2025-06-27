import fitz  # PyMuPDF
import spacy
import os
import docx
import streamlit as st
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer, util
from io import StringIO
import tempfile

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





