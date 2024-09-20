import streamlit as st
from langchain_ollama import OllamaLLM
import json

model = OllamaLLM(model='llama3')

st.title("MCQ Generator")

category = st.selectbox("Select Category", ["Aptitude", "Computer Science"])

def generate_mcqs(category):
    prompt = f"Generate 5 multiple-choice questions with 4 options each on {category}. Provide the correct answer as well."
    
    mcq_data = model.invoke(input=prompt)
    
    return mcq_data

if st.button("Generate MCQs"):
    if category:
        mcqs_data = generate_mcqs(category)
        
        try:
            mcqs = json.loads(mcqs_data)
        except json.JSONDecodeError:
            st.error("Error parsing MCQs data. The format might be incorrect.")
            st.write(mcqs_data)  
            mcqs = [] 
        
        if not mcqs:
            st.error("No MCQs generated. Please try again.")
        else:
            st.session_state.mcqs = mcqs  
            
            st.subheader(f"MCQs for {category}")
            st.session_state.user_answers = []
            
            for i, mcq in enumerate(mcqs):
                st.write(f"**Q{i+1}: {mcq['question']}**")
                options = mcq['options']
                user_answer = st.selectbox(f"Choose the correct option for Q{i+1}", options, key=f'q{i+1}')
                st.session_state.user_answers.append(user_answer)
            
            if st.button("Submit Answers"):
                score = 0
                for i, mcq in enumerate(mcqs):
                    correct_answer = mcq['answer']
                    user_answer = st.session_state.user_answers[i]
                    if user_answer == correct_answer:
                        score += 1
                
                st.subheader("Your Score")
                st.write(f"You answered {score} out of {len(mcqs)} questions correctly.")
                
    else:
        st.error("Please select a category.")
