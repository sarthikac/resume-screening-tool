import fitz
import spacy
import os
import streamlit as st
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer, util
from io import StringIO
import tempfile

nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")
SUPPORTED_TYPES = ("pdf", "docx", "txt")



