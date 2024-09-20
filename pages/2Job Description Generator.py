import streamlit as st
from langchain_ollama import OllamaLLM


if 'user_role' not in st.session_state:
    st.error("Please log in to access this page.")
elif st.session_state.user_role == 'hr':
    model = OllamaLLM(model='llama3')

    st.title("Job Description Generator")

    job_title = st.text_input("Enter the Job Title")
    experience_level = st.selectbox("Select Experience Level", ["Entry-level", "Mid-level", "Senior-level"])

    if st.button("Generate Job Description"):
        if job_title and experience_level:
            prompt = f"Generate a detailed job description for a {experience_level} {job_title}. Include key responsibilities, required skills, qualifications, and any other relevant details."
            
            job_description = model.invoke(input=prompt)
            
            st.subheader("Generated Job Description")
            st.write(job_description)
        else:
            st.error("Please enter both job title and experience level.")
else:
    st.error("You do not have access to this page.")      
        
        
        
        
