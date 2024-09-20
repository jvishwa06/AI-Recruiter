import streamlit as st
st.session_state.current_page = "Page1"
st.title("AI based Ethical Hiring Platform Workflow")

workflow_steps = [
    "1. **Job Description Generation**: The platform uses a large language model (LLM) to generate a specific and detailed job description tailored to the requirements of the position.",
    "2. **Resume Submission**: Candidates submit their resumes through the platform.",
    "3. **Candidate Profile Extension**: If any information is missing from a candidate’s resume, the platform asks additional questions to complete their profile and provide a comprehensive view of their qualifications."
    "4. **Resume Screening and Bias Removal**: The platform processes the uploaded resumes, removing personal identifiers such as names, gender, and ethnicity to ensure unbiased evaluation.",
    "5. **Resume and Project Analysis**: The platform analyzes the resumes and verifies project details on platforms like GitHub. It assesses the performance and relevance of the candidate's experience.",
    "6. **Personalized Interview Questions**: Based on the analyzed resume and project details, the Conversational AI generates personalized interview questions tailored to each candidate’s background and skills.",
    "7. **Real-Time Interview Interaction**: During the interview, the Conversational AI provides real-time responses and feedback, ensuring a smooth and engaging interaction with the candidate.",
    "8. **Sentiment Analysis**: The platform evaluates the candidate’s facial expressions and voice responses during the interview to gauge their confidence levels and soft skills.",
    "9. **Cheat-Proof Recruitment Environment**: The platform implements measures such as camera monitoring, lip-sync verification, tab-switching detection, and kernel-level tools to prevent cheating and ensure a fair recruitment process.",
    "10. **Explainable AI for Decision Making**: After the interview and evaluation process, the platform uses Explainable AI to provide clear reasons for selecting or rejecting candidates, ensuring transparency in the decision-making process.",
    "11. **Customer Support**: A dedicated LLM handles customer support queries, providing assistance and resolving issues promptly.",
]

# Display workflow steps
st.subheader("Workflow Steps")
for step in workflow_steps:
    st.write(step)
