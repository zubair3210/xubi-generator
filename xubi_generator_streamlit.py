import streamlit as st
from fpdf import FPDF
import re
import random
import tempfile

def parse_questions(uploaded_file):
    if not uploaded_file:
        return []
    content = uploaded_file.read().decode("utf-8")
    q_blocks = re.split(r"\n\s*\n", content.strip())
    questions = [q.strip() for q in q_blocks if q.strip()]
    return questions

def generate_pdf(book, chapter, mcqs, shorts, longs, mcq_count, short_count, long_count, include_mcq, include_short, include_long):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, book, ln=True, align="C")
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Chapter: {chapter}", ln=True, align="C")

    if include_mcq and mcqs:
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "MCQs", ln=True)
        selected = random.sample(mcqs, min(mcq_count, len(mcqs)))
        for idx, q in enumerate(selected, 1):
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 10, f"{idx}. {q}")

    if include_short and shorts:
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Short Questions", ln=True)
        selected = random.sample(shorts, min(short_count, len(shorts)))
        for idx, q in enumerate(selected, 1):
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 10, f"{idx}. {q}")

    if include_long and longs:
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Long Questions", ln=True)
        selected = random.sample(longs, min(long_count, len(longs)))
        for idx, q in enumerate(selected, 1):
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 10, f"{idx}. {q}")

    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_pdf.name)
    return temp_pdf.name

# ----- Streamlit UI -----
st.set_page_config(page_title="Xubi Generator", layout="centered")
st.markdown("<h1 style='text-align: center; color: #39ff14;'>Xubi Generator</h1>", unsafe_allow_html=True)

book = st.text_input("📘 Book Name")
chapter = st.text_input("📖 Chapter Name")

st.markdown("### 📂 Upload Your Files")
mcq_file = st.file_uploader("Upload MCQs (.txt)", type="txt")
short_file = st.file_uploader("Upload Short Questions (.txt)", type="txt")
long_file = st.file_uploader("Upload Long Questions (.txt)", type="txt")

st.markdown("### ✅ Select Question Types & Quantity")
include_mcq = st.checkbox("Include MCQs", value=True)
mcq_count = st.number_input("Number of MCQs", min_value=0, value=10) if include_mcq else 0

include_short = st.checkbox("Include Short Questions", value=True)
short_count = st.number_input("Number of Short Questions", min_value=0, value=10) if include_short else 0

include_long = st.checkbox("Include Long Questions", value=True)
long_count = st.number_input("Number of Long Questions", min_value=0, value=3) if include_long else 0

if st.button("🚀 Generate PDF"):
    if not book or not chapter:
        st.error("Please enter both Book and Chapter name.")
    else:
        mcqs = parse_questions(mcq_file) if include_mcq else []
        shorts = parse_questions(short_file) if include_short else []
        longs = parse_questions(long_file) if include_long else []

        pdf_path = generate_pdf(book, chapter, mcqs, shorts, longs,
                                mcq_count, short_count, long_count,
                                include_mcq, include_short, include_long)

        with open(pdf_path, "rb") as f:
            st.success("🎉 PDF generated successfully!")
            st.download_button("📥 Download PDF", f.read(), file_name="Xubi_Generated.pdf", mime="application/pdf")
