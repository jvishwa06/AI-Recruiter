import streamlit as st
import requests
import re
from langchain_ollama import OllamaLLM

model = OllamaLLM(model='llama3')

st.title("Chat with GitHub Repository")

def download_md_files(repo_url, token):
    repo_name = re.search(r'github.com/([^/]+/[^/]+)', repo_url).group(1)
    
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

def create_prompt(text):
    return (
        f"Please provide detailed information and context based on the following content. "
        f"Here is the text:\n\n{text}"
    )

def chat_with_model(content, question):
    prompt = create_prompt(content) + f"\n\nUser question: {question}"
    response = model.invoke(input=prompt)
    return response

st.header("GitHub Repository Chat")

repo_url = st.text_input("Enter GitHub Repository URL")
github_token = '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'

if repo_url and github_token:
    try:
        md_files = download_md_files(repo_url, github_token)
        
        if md_files:
            combined_md_content = "\n".join(md_files)
            
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
