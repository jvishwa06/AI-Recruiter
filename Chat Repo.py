import streamlit as st
import requests
import re
from langchain_ollama import OllamaLLM

# Initialize the Ollama model
model = OllamaLLM(model='llama3')

# Streamlit application layout
st.title("Chat with GitHub Repository")

# Function to download markdown files from a GitHub repository
def download_md_files(repo_url, token):
    repo_name = re.search(r'github.com/([^/]+/[^/]+)', repo_url).group(1)
    
    # Get repository contents
    contents_url = f"https://api.github.com/repos/{repo_name}/contents"
    headers = {'Authorization': f'token {token}'}
    response = requests.get(contents_url, headers=headers)
    contents = response.json()
    
    md_files = []
    for file in contents:
        if file['type'] == 'file' and file['name'].endswith('.md'):
            file_url = file['download_url']
            file_response = requests.get(file_url)
            md_files.append(file_response.text)
    
    return md_files

# Function to create a prompt for the LLM
def create_prompt(text):
    return (
        f"Please provide detailed information and context based on the following content. "
        f"Here is the text:\n\n{text}"
    )

# Function to use the LLM to generate responses
def chat_with_model(content, question):
    prompt = create_prompt(content) + f"\n\nUser question: {question}"
    response = model.invoke(input=prompt)
    return response

# Streamlit Interface
st.header("GitHub Repository Chat")

# Input for GitHub Repository and Token
repo_url = st.text_input("Enter GitHub Repository URL")
github_token = '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'

if repo_url and github_token:
    try:
        # Download .md files
        md_files = download_md_files(repo_url, github_token)
        
        if md_files:
            # st.write("*Markdown Files Content*:")
            combined_md_content = "\n".join(md_files)
            # st.text_area('Combined Markdown Content', combined_md_content, height=300)
            
            # Chat with Ollama
            st.header('Ask Questions About the Repository')
            user_question = st.text_input('Type your question here')
            
            if user_question:
                response = chat_with_model(combined_md_content, user_question)
                st.write(f"{response}")
        else:
            st.write("No markdown files found in the repository.")
    
    except Exception as e:
        st.write(f"Error: {str(e)}")
else:
    st.write("Please provide the GitHub repository URL.")