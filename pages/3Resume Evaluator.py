import streamlit as st
import PyPDF2  
import mammoth  
from langchain_ollama import OllamaLLM



if 'user_role' not in st.session_state:
    st.error("Please log in to access this page.")
elif st.session_state.user_role == 'hr':

    model = OllamaLLM(model='llama3')

    st.title("Resume Evaluator")

    uploaded_file = st.file_uploader("Upload a PDF or Word Document", type=['pdf', 'docx'])

    job_description = st.text_area("Paste Job Description Here", height=200)

    def extract_pdf_text(pdf_file):
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    def extract_docx_text(docx_file):
        result = mammoth.extract_raw_text(docx_file)
        return result.value

    def create_prompt(text):
        return (
            f"Please organize the following text into structured information. Focus on extracting skills, education, "
            f"experience, certifications, and projects. Remove any references to gender, race, or nationality. "
            f"Here is the text:\n\n{text}"
        )

    def compare_resume_job_description(resume_data, job_description):
        return (
            f"Based on the resume data below and the job description provided, please compare the two and return a plain "
            f"text report highlighting which skills, tools, and qualifications match, and which are missing. Also provide "
            f"a relevance score between 0 and 100 for the candidate’s fit for the role.\n\n"
            f"Resume Data:\n{resume_data}\n\n"
            f"Job Description:\n{job_description}"
        )

    def save_structured_data_to_file(structured_data):
        with open("structured_resume_data.txt", "w") as file:
            file.write(structured_data)

    def display_score(response):
        lines = response.splitlines()
        for line in lines:
            if "Score" in line:
                return line
        return "No score provided"

    if st.button("Start Analysis"):
        if uploaded_file and job_description:
            if uploaded_file.name.endswith('.pdf'):
                extracted_text = extract_pdf_text(uploaded_file)
            elif uploaded_file.name.endswith('.docx'):
                extracted_text = extract_docx_text(uploaded_file)

            resume_prompt = create_prompt(extracted_text)
            
            structured_data = model.invoke(input=resume_prompt)
            
            save_structured_data_to_file(structured_data)
            
            comparison_prompt = compare_resume_job_description(structured_data, job_description)
            
            comparison_result = model.invoke(input=comparison_prompt)
            
            st.subheader("Job Description Relevance and Analysis")
            st.write(comparison_result)

            final_score = display_score(comparison_result)
            st.subheader(f"Candidate Relevance Score: {final_score}")

        else:
            st.write("Please upload a resume file and provide a job description for analysis.")
else:
    st.error("You do not have access to this page.")