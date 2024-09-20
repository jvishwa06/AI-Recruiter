import streamlit as st
import PyPDF2  # PyPDF2 for PDF extraction
import mammoth  # mammoth for Word file extraction
from langchain_ollama import OllamaLLM


if 'user_role' not in st.session_state:
    st.error("Please log in to access this page.")
elif st.session_state.user_role == 'hr':
    st.title("Page 1 - Employee and HR Access")
    st.write("Welcome! This page is accessible by both employees and HR.")

    # Initialize the Ollama model
    model = OllamaLLM(model='llama3')

    # Streamlit application layout
    st.title("Resume Scanner")

    # File uploader for PDF and DOCX files
    uploaded_file = st.file_uploader("Upload a PDF or Word Document", type=['pdf', 'docx'])

    # Function to extract text from PDF using PyPDF2
    def extract_pdf_text(pdf_file):
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    # Function to extract text from Word (.docx) using mammoth
    def extract_docx_text(docx_file):
        result = mammoth.extract_raw_text(docx_file)
        return result.value

    # Function to generate a custom prompt for the LLM
    def create_prompt(text):
        return (
        f"Please organize the following resume text into structured data while separating unbiased and biased information into two JSON files.\n\n"

        f"### Instructions:\n\n"

        f"1. File 1: Extract relevant details such as skills, education, experience, certifications, and projects.\n"
        f"Ensure that any references to gender, race, nationality, or other potentially biased terms are excluded. Use the following keys:\n"
        f"- skills: List of skills mentioned.\n"
        f"- education: Degrees, institutions, and graduation years.\n"
        f"- experience: Job titles, companies, durations, and responsibilities.\n"
        f"- certifications: Certifications with name, institution, and year.\n"
        f"- projects: Key projects with descriptions, technologies used, and the candidate’s role.\n"
        f"- other attributes: Any additional unbiased attributes contributing to the candidate's selection.\n"
        f"- bias ID: A unique identifier to link this file with File 2.\n\n"
        f"Exclude personal information and biased terms from this file.\n\n"

        f"2. File 2: Extract all the biased information that was excluded from File 1.\n"
        f"Include any details related to gender, race, nationality, and other demographic information under the following keys:\n"
        f"- gender: Gender, if mentioned.\n"
        f"- race: Race or ethnicity, if mentioned.\n"
        f"- nationality: Nationality or citizenship.\n"
        f"- age: Age or date of birth, if mentioned.\n"
        f"- religion: Religion, if mentioned.\n"
        f"- marital status: Marital status, if mentioned.\n"
        f"- other biased terms: Any other biased terms.\n"
        f"- bias ID: The same unique identifier from File 1.\n\n"
        f"Include personal information and any biased terms in this file.\n\n"

        f"Here is the resume text:\n\n{text}"
        )

    # Automatically process and structure data
    if uploaded_file:
        # Check if the uploaded file is a PDF or Word document
        if uploaded_file.name.endswith('.pdf'):
            extracted_text = extract_pdf_text(uploaded_file)
        elif uploaded_file.name.endswith('.docx'):
            extracted_text = extract_docx_text(uploaded_file)

        # Generate the prompt for the LLM
        prompt = create_prompt(extracted_text)
        
        # Use the Ollama model to process the text
        structured_data = model.invoke(input=prompt)
        
        st.subheader("Structured Data")
        st.write(structured_data)

    else:
        st.write("Please upload a file to extract data.")
else:
    st.error("You do not have access to this page.")