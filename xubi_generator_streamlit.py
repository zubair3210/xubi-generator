import streamlit as st
from fpdf import FPDF
import re
import random
import tempfile
import os

# FPDF subclass for DejaVu font setup
class PDF(FPDF):
    def header(self):
        pass  # Disable default header

    def footer(self):
        pass  # Disable default footer

def clean_question_text(text):
    # Replace multiple newlines/spaces with single space
    text = re.sub(r'\s*\n\s*', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def parse_questions(file):
    content = file.read().decode("utf-8")
    q_blocks = re.split(r"\n\s*\n", content.strip())
    questions = [q.strip() for q in q_blocks if q.strip()]
    return questions

def generate_pdf(book, chapter, mcqs, shorts, longs, mcq_count, short_count, long_count,
                 include_mcq, include_short, include_long):

    pdf = PDF()
    pdf.add_page()

    # Add DejaVu font for unicode support
    font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
    if not os.path.exists(font_path):
        st.error("Font file DejaVuSans.ttf not found in the app directory!")
        return None
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.add_font("DejaVu", "B", font_path, uni=True)

    # Header
    pdf.set_font("DejaVu", "B", 16)
    pdf.cell(0, 10, book, ln=True, align="C")
    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 10, f"Chapter: {chapter}", ln=True, align="C")
    pdf.ln(10)

    # MCQs Section
    if include_mcq and mcqs:
        pdf.set_font("DejaVu", "B", 14)
        pdf.cell(0, 10, "MCQs", ln=True)
        selected = random.sample(mcqs, min(mcq_count, len(mcqs)))
        pdf.set_font("DejaVu", "", 12)
        for idx, q in enumerate(selected, 1):
            cleaned_q = clean_question_text(q)
            pdf.multi_cell(0, 8, f"{idx}. {cleaned_q}")
            pdf.ln(2)

    # Short Questions Section
    if include_short and shorts:
        pdf.set_font("DejaVu", "B", 14)
        pdf.cell(0, 10, "Short Questions", ln=True)
        selected = random.sample(shorts, min(short_count, len(shorts)))
        pdf.set_font("DejaVu", "", 12)
        for idx, q in enumerate(selected, 1):
            cleaned_q = clean_question_text(q)
            pdf.multi_cell(0, 8, f"{idx}. {cleaned_q}")
            pdf.ln(2)

    # Long Questions Section
    if include_long and longs:
        pdf.set_font("DejaVu", "B", 14)
        pdf.cell(0, 10, "Long Questions", ln=True)
        selected = random.sample(longs, min(long_count, len(longs)))
        pdf.set_font("DejaVu", "", 12)
        for idx, q in enumerate(selected, 1):
            cleaned_q = clean_question_text(q)
            pdf.multi_cell(0, 8, f"{idx}. {cleaned_q}")
            pdf.ln(2)

    # Save PDF to a temporary file and return its path
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_pdf.name)
    return temp_pdf.name

# Streamlit UI
st.title("Xubi Generator (Online)")

book = st.text_input("Book Name:")
chapter = st.text_input("Chapter:")

uploaded_mcq = st.file_uploader("Upload MCQs File (.txt)", type=["txt"])
uploaded_short = st.file_uploader("Upload Short Questions File (.txt)", type=["txt"])
uploaded_long = st.file_uploader("Upload Long Questions File (.txt)", type=["txt"])

include_mcq = st.checkbox("Include MCQs")
include_short = st.checkbox("Include Short Questions")
include_long = st.checkbox("Include Long Questions")

mcq_count = st.number_input("Number of MCQs", min_value=0, max_value=1000, value=10)
short_count = st.number_input("Number of Short Questions", min_value=0, max_value=1000, value=17)
long_count = st.number_input("Number of Long Questions", min_value=0, max_value=1000, value=3)

mcqs = []
shorts = []
longs = []

if uploaded_mcq:
    mcqs = parse_questions(uploaded_mcq)
if uploaded_short:
    shorts = parse_questions(uploaded_short)
if uploaded_long:
    longs = parse_questions(uploaded_long)

if st.button("Generate PDF"):
    if not book.strip() or not chapter.strip():
        st.error("Please enter both Book name and Chapter.")
    elif (include_mcq and not mcqs) and (include_short and not shorts) and (include_long and not longs):
        st.error("Please upload at least one question file matching the selected sections.")
    else:
        pdf_path = generate_pdf(book, chapter, mcqs, shorts, longs,
                                mcq_count, short_count, long_count,
                                include_mcq, include_short, include_long)
        if pdf_path:
            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF", f, file_name=f"{book}_Chapter_{chapter}.pdf")
            # Cleanup temp file after download
            os.remove(pdf_path)
