import streamlit as st
import PyPDF2  # PyPDF2 for PDF extraction
import mammoth  # mammoth for Word file extraction
from langchain_ollama import OllamaLLM

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
        f"Please organize the following text into structured data while removing any biased information. "
        f"Focus on extracting skills, education, experience, certifications, and projects. "
        f"remove gender, race, nationality from it"
        f"Ensure that any references to gender, race, nationality, or other potentially biased terms are excluded. "
        f"Here is the text:\n\n{text}"
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