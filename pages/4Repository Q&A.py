import streamlit as st
import requests
import re
from langchain_ollama import OllamaLLM

if 'user_role' not in st.session_state:
    st.error("Please log in to access this page.")
elif st.session_state.user_role == 'employee' or st.session_state.user_role == 'hr' :

    model = OllamaLLM(model='llama3')

    GITHUB_TOKEN = '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'

    st.title("GitHub Repository QA")

    def download_md_files(repo_url, token):
        repo_name = re.search(r'github.com/([^/]+/[^/]+)', repo_url).group(1)
        
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

    def generate_hard_question_prompt(text):
        return (
  f"You are a technical recruiter evaluating a candidate's project submission. Below is the data extracted from the README.md file from their GitHub project. "
  f"Your task is to generate a single in-depth and probing question to assess the candidate's understanding of the project, their decisions, the technologies used, and the overall execution."
  
  f"### Evaluation Areas to Cover: "
  f"\n1. *Understanding of the problem the project solves*: Is the candidate clear about the core issue the project is addressing?"
  f"\n2. *Methodology, frameworks, and tools used*: Can they explain why they chose specific tools or frameworks? Do they understand their limitations and advantages?"
  f"\n3. *Design decisions and rationale*: Why did they make particular architectural or design choices? What trade-offs were considered?"
  f"\n4. *Challenges encountered and resolutions*: What were the major roadblocks, and how did the candidate approach solving them?"
  f"\n5. *Potential improvements or optimizations*: Are there areas where the project could be improved? How would they enhance its efficiency or performance?"
  f"\n6. *Scalability and future scope*: Can the project scale effectively? What changes would be necessary to accommodate a larger user base?"
  f"\n7. *Project performance, efficiency, and testing*: How did they ensure the project runs efficiently? What testing methodologies were employed?"
  f"\n8. *Collaboration or teamwork*: If applicable, how did they collaborate with others during the project? What tools were used for collaboration?"
  f"\n9. *Real-world application*: How does this project relate to real-world scenarios? What value or impact does it have?"
  
  f"Generate a *single, in-depth question* based on the input data that comprehensively evaluates the candidate’s understanding of one or more of the above criteria."
  
  f"Only include criteria that can be evaluated based on the given project data."
  f"give only question as response dont include metrics or other things and also dont add introduction to question, give only the question "
  
  f"\nProject details:\n{text}" 
        )

    def evaluate_answer_and_score_prompt(question, user_answer, project_description):
        return (
  f"Here is a project description, a hard-level question, and the user's answer. "
  f"Provide a detailed evaluation of the answer and give a score from 1 to 10 based on the following criteria, which are essential for selecting a candidate: "
  f"\n1. *Correctness*: How accurately does the answer address the question? Does it reflect an understanding of the core concepts?"
  f"\n2. *Depth*: Does the answer demonstrate a deep knowledge of the subject? Are key technical details, considerations, or advanced concepts included?"
  f"\n3. *Relevance*: Does the answer stay focused on the question and project? Are the points raised relevant to the specific context of the project and problem?"
  f"\n4. *Problem-Solving*: Does the answer show the ability to address potential challenges, bottlenecks, or future considerations?"
  f"\n5. *Clarity*: Is the explanation easy to understand, well-structured, and logically presented?"
  
  f"Score the response on each of these criteria (from 1 to 10), and give a final score out of 10 based on the overall quality of the response."

  f"\nProject description:\n{project_description}\n\n"
  f"Question: {question}\n\n"
  f"User's Answer: {user_answer}" 

        )

    def interact_with_model(prompt):
        response = model.invoke(input=prompt)
        return response

    repo_url = st.text_input("Enter GitHub Repository URL")

    if repo_url:
        try:
            md_files = download_md_files(repo_url, GITHUB_TOKEN)
            
            if md_files:
                combined_md_content = "\n".join(md_files)
                
                question_prompt = generate_hard_question_prompt(combined_md_content)
                question_response = interact_with_model(question_prompt)
                hard_question = question_response.strip()  
                st.write(f"{hard_question}")
                
                user_answer = st.text_area("Your answer", placeholder="Type your answer here")
                
                if st.button("Submit Answer"):
                    if user_answer:
                        evaluation_prompt = evaluate_answer_and_score_prompt(hard_question, user_answer, combined_md_content)
                        evaluation_response = interact_with_model(evaluation_prompt)
                        
                        st.write(f"Evaluation and Score:\n{evaluation_response}")
                    else:
                        st.write("Please provide an answer to the question.")
            else:
                st.write("No markdown files found in the repository.")
        
        except Exception as e:
            st.write(f"Error: {str(e)}")
    else:
        st.write("Please enter a GitHub repository URL.")
else:
    st.error("You do not have access to this page.")