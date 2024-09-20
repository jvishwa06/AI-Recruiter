import streamlit as st
from langchain_ollama import OllamaLLM


llm = OllamaLLM(model="llama3")

def main():
    st.title("Chat with Ollama LLM")
    user_input = st.text_input("You:", "")
    if user_input:
        try:
            response = llm.invoke(input=user_input)  
            st.write(f"Bot: {response}")
        except Exception as e:
            st.write(f"Error: {e}")

if __name__ == "__main__":
    main()
