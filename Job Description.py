import streamlit as st
from langchain_ollama import OllamaLLM

# Initialize the Ollama model
model = OllamaLLM(model='llama3')

# Streamlit application layout
st.title("Job Description Generator")

# Input fields for job title and experience level
job_title = st.text_input("Enter the Job Title")
experience_level = st.selectbox("Select Experience Level", ["Entry-level", "Mid-level", "Senior-level"])

# Generate job description based on inputs
if st.button("Generate Job Description"):
    if job_title and experience_level:
        # Construct the prompt for the language model
        prompt = f"Generate a detailed job description for a {experience_level} {job_title}. Include key responsibilities, required skills, qualifications, and any other relevant details."
        
        # Use the Ollama model to generate the job description
        job_description = model.invoke(input=prompt)
        
        st.subheader("Generated Job Description")
        st.write(job_description)
    else:
        st.error("Please enter both job title and experience level.")
