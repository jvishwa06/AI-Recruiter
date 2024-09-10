import streamlit as st
import requests
import re
from langchain_ollama import OllamaLLM

# Initialize the Ollama model
model = OllamaLLM(model='llama3')

# Fixed GitHub token
GITHUB_TOKEN = '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'

# Streamlit application layout
st.title("GitHub Repository QA")

# Function to download markdown files from a GitHub repository
def download_md_files(repo_url, token):
    repo_name = re.search(r'github.com/([^/]+/[^/]+)', repo_url).group(1)
    
    # Get repository contents
    contents_url = f"https://api.github.com/repos/{repo_name}/contents"
    headers = {'Authorization': f'token ' + token}
    response = requests.get(contents_url, headers=headers)
    contents = response.json()
    
    md_files = []
    for file in contents:
        if file['type'] == 'file' and file['name'].endswith('.md'):
            file_url = file['download_url']
            file_response = requests.get(file_url)
            md_files.append(file_response.text)
    
    return md_files

# Function to generate a single hard-level question
def generate_hard_question_prompt(text):
    return (
        f"Based on the following content, generate 1 hard-level question that tests deep understanding of the project, "
        f"focusing on advanced concepts, algorithms, and techniques used. Here is the text:\n\n{text}"
    )

# Function to create a prompt for evaluating the user's answer and scoring it
def evaluate_answer_and_score_prompt(question, user_answer, project_description):
    return (
        f"Here is a project description and a hard-level question along with the user's answer. "
        f"Provide a detailed evaluation of the answer and give a score from 1 to 10 based on the correctness, depth, and relevance. "
        f"\nProject description:\n{project_description}\n\n"
        f"Question: {question}\n\n"
        f"User's Answer: {user_answer}"
    )

# Function to interact with the model
def interact_with_model(prompt):
    response = model.invoke(input=prompt)
    return response

# Streamlit Interface
st.header("GitHub Repository Question and Answer")

# Input for GitHub Repository URL
repo_url = st.text_input("Enter GitHub Repository URL")

if repo_url:
    try:
        # Download .md files
        md_files = download_md_files(repo_url, GITHUB_TOKEN)
        
        if md_files:
            combined_md_content = "\n".join(md_files)
            
            # Generate one hard-level question
            question_prompt = generate_hard_question_prompt(combined_md_content)
            question_response = interact_with_model(question_prompt)
            hard_question = question_response.strip()  # Assuming the question is returned as a single response
            
            # Display the hard question
            st.write(f"Hard-Level Question: {hard_question}")
            
            # Capture user's answer
            user_answer = st.text_area("Your answer", placeholder="Type your answer here")
            
            # Evaluate the user's answer once submitted
            if st.button("Submit Answer"):
                if user_answer:
                    evaluation_prompt = evaluate_answer_and_score_prompt(hard_question, user_answer, combined_md_content)
                    evaluation_response = interact_with_model(evaluation_prompt)
                    
                    # Display evaluation and score
                    st.write(f"Evaluation and Score:\n{evaluation_response}")
                else:
                    st.write("Please provide an answer to the question.")
        else:
            st.write("No markdown files found in the repository.")
    
    except Exception as e:
        st.write(f"Error: {str(e)}")
else:
    st.write("Please enter a GitHub repository URL.")