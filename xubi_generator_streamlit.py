import streamlit as st
from fpdf import FPDF
import re
import random
import tempfile
import os

# ✅ Function to read questions
def parse_questions(uploaded_file):
    if uploaded_file is None:
        return []
    content = uploaded_file.read().decode("utf-8")
    blocks = re.split(r"\n\s*\n", content.strip())
    return [q.strip() for q in blocks if q.strip()]

# ✅ PDF Generator
def generate_pdf(book, chapter, mcqs, shorts, longs,
                 mcq_count, short_count, long_count,
                 include_mcq, include_short, include_long):
    
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 16)

    pdf.cell(0, 10, book, ln=True, align="C")
    pdf.set_font('DejaVu', '', 14)
    pdf.cell(0, 10, f"Chapter: {chapter}", ln=True, align="C")

    if include_mcq:
        pdf.cell(0, 10, "MCQs", ln=True)
        selected = random.sample(mcqs, min(mcq_count, len(mcqs)))
        for idx, q in enumerate(selected, 1):
            pdf.multi_cell(0, 10, f"{idx}. {q}")

    if include_short:
        pdf.cell(0, 10, "Short Questions", ln=True)
        selected = random.sample(shorts, min(short_count, len(shorts)))
        for idx, q in enumerate(selected, 1):
            pdf.multi_cell(0, 10, f"{idx}. {q}")

    if include_long:
        pdf.cell(0, 10, "Long Questions", ln=True)
        selected = random.sample(longs, min(long_count, len(longs)))
        for idx, q in enumerate(selected, 1):
            pdf.multi_cell(0, 10, f"{idx}. {q}")

    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_pdf.name)
    return temp_pdf.name

# ✅ Streamlit App UI
st.title("📘 Xubi Generator - Online PDF Tool")
st.markdown("Easily generate custom exam PDFs with selected questions.")

book = st.text_input("Book Name:")
chapter = st.text_input("Chapter Name:")

uploaded_mcq = st.file_uploader("Upload MCQs File (.txt)", type="txt")
uploaded_short = st.file_uploader("Upload Short Questions File (.txt)", type="txt")
uploaded_long = st.file_uploader("Upload Long Questions File (.txt)", type="txt")

include_mcq = st.checkbox("Include MCQs")
mcq_count = st.number_input("How many MCQs?", min_value=0, step=1) if include_mcq else 0

include_short = st.checkbox("Include Short Questions")
short_count = st.number_input("How many Short Questions?", min_value=0, step=1) if include_short else 0

include_long = st.checkbox("Include Long Questions")
long_count = st.number_input("How many Long Questions?", min_value=0, step=1) if include_long else 0

if st.button("Generate PDF"):
    mcqs = parse_questions(uploaded_mcq)
    shorts = parse_questions(uploaded_short)
    longs = parse_questions(uploaded_long)

    pdf_path = generate_pdf(book, chapter, mcqs, shorts, longs,
                            mcq_count, short_count, long_count,
                            include_mcq, include_short, include_long)

    with open(pdf_path, "rb") as f:
        st.download_button("📥 Download PDF", f, file_name="xubi_generated.pdf")

    os.remove(pdf_path)
