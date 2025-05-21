import streamlit as st
from fpdf import FPDF
import re
import random
import tempfile

# Ensure DejaVuSans.ttf is in your working directory or provide full path
FONT_PATH = "DejaVuSans.ttf"

def parse_questions(content):
    q_blocks = re.split(r"\n\s*\n", content.strip())
    questions = [q.strip() for q in q_blocks if q.strip()]
    return questions

def generate_pdf(book, chapter, mcqs, shorts, longs,
                 mcq_count, short_count, long_count,
                 include_mcq, include_short, include_long):
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(10, 10, 10)
    
    # Add DejaVu font for Unicode support
    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.add_font("DejaVu", "B", FONT_PATH, uni=True)
    
    # Header
    pdf.set_font("DejaVu", "B", 16)
    pdf.cell(0, 10, book, ln=True, align="C")
    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 10, f"Chapter: {chapter}", ln=True, align="C")

    # MCQs
    if include_mcq:
        pdf.set_font("DejaVu", "B", 14)
        pdf.cell(0, 10, "MCQs", ln=True)
        selected = random.sample(mcqs, min(mcq_count, len(mcqs)))
        for idx, q in enumerate(selected, 1):
            pdf.set_font("DejaVu", "", 12)
            pdf.multi_cell(180, 10, f"{idx}. {q}")

    # Short Questions
    if include_short:
        pdf.set_font("DejaVu", "B", 14)
        pdf.cell(0, 10, "Short Questions", ln=True)
        selected = random.sample(shorts, min(short_count, len(shorts)))
        for idx, q in enumerate(selected, 1):
            pdf.set_font("DejaVu", "", 12)
            pdf.multi_cell(180, 10, f"{idx}. {q}")

    # Long Questions
    if include_long:
        pdf.set_font("DejaVu", "B", 14)
        pdf.cell(0, 10, "Long Questions", ln=True)
        selected = random.sample(longs, min(long_count, len(longs)))
        for idx, q in enumerate(selected, 1):
            pdf.set_font("DejaVu", "", 12)
            pdf.multi_cell(180, 10, f"{idx}. {q}")

    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_pdf.name)
    return temp_pdf.name

st.title("Xubi Generator - Online PDF Generator")

book = st.text_input("Book Name:")
chapter = st.text_input("Chapter Name:")

include_mcq = st.checkbox("Include MCQs")
mcq_count = st.number_input("Number of MCQs", min_value=0, max_value=100, value=10)

include_short = st.checkbox("Include Short Questions")
short_count = st.number_input("Number of Short Questions", min_value=0, max_value=100, value=10)

include_long = st.checkbox("Include Long Questions")
long_count = st.number_input("Number of Long Questions", min_value=0, max_value=100, value=3)

mcq_file = st.file_uploader("Upload MCQs Text File", type=["txt"])
short_file = st.file_uploader("Upload Short Questions Text File", type=["txt"])
long_file = st.file_uploader("Upload Long Questions Text File", type=["txt"])

if st.button("Generate PDF"):
    if not book or not chapter:
        st.error("Please enter both Book Name and Chapter.")
    else:
        mcqs = []
        shorts = []
        longs = []
        try:
            if include_mcq and mcq_file is not None:
                mcqs = parse_questions(mcq_file.read().decode("utf-8"))
            if include_short and short_file is not None:
                shorts = parse_questions(short_file.read().decode("utf-8"))
            if include_long and long_file is not None:
                longs = parse_questions(long_file.read().decode("utf-8"))
            
            pdf_path = generate_pdf(book, chapter, mcqs, shorts, longs,
                                    mcq_count, short_count, long_count,
                                    include_mcq, include_short, include_long)
            
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            st.success("PDF generated successfully!")
            st.download_button("Download PDF", data=pdf_bytes, file_name="Xubi_Generated.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"Error: {e}")
