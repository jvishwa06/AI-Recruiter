import streamlit as st
import ollama as ol
from streamlit_mic_recorder import speech_to_text

if 'user_role' not in st.session_state:
    st.error("Please log in to access this page.")
elif st.session_state.user_role == 'employee' or st.session_state.user_role == 'hr' :
    def record_voice():
        # Initialize session state
        state = st.session_state

        if "text_received" not in state:
            state.text_received = []

        text = speech_to_text(
            start_prompt="Click and speak to answer the question",
            stop_prompt="Stop recording ⚠️",
            language="en",  # Language set to English by default
            use_container_width=True,
            just_once=True,
        )

        if text:
            state.text_received.append(text)

        result = "".join(state.text_received)
        state.text_received = []  # Clear received text

        return result if result else None

    # st.set_page_config(page_title="🎙️ Voice Bot", layout="wide")
    st.title("🎙️ AI Interviewer")
    st.sidebar.title("🎙️ Speech-to-Text Recorder")

    # Set default model and language
    MODEL = "llama3"
    LANGUAGE = "en"

    def print_txt(text):
        # If the text contains Arabic characters, align it accordingly
        if any("\u0600" <= c <= "\u06FF" for c in text):  # check if text contains Arabic characters
            text = f"<p style='direction: rtl; text-align: right;'>{text}</p>"
        st.markdown(text, unsafe_allow_html=True)

    def print_chat_message(message):
        text = message["content"]
        if message["role"] == "user":
            with st.chat_message("user", avatar="🎙️"):
                print_txt(text)
        else:
            with st.chat_message("assistant", avatar="🦙"):
                print_txt(text)

    def main():
        # Initialize chat history for the default model
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = {}
        if MODEL not in st.session_state.chat_history:
            st.session_state.chat_history[MODEL] = [
                {"role": "assistant", "content": "Hello! I'm your interviewer today. Let's start with a simple question: Tell me about yourself?"}
            ]
        
        chat_history = st.session_state.chat_history[MODEL]

        # Display start/stop recording in the sidebar
        with st.sidebar:
            user_response = record_voice()

        # Print conversation history
        for message in chat_history:
            print_chat_message(message)

        # If there is a user response (voice converted to text)
        if user_response:
            user_message = {"role": "user", "content": user_response}
            print_chat_message(user_message)
            chat_history.append(user_message)
            
            # Get response from the LLM (simulating an interviewer asking a follow-up question)
            response = ol.chat(model=MODEL, messages=chat_history)
            answer = response['message']['content']
            ai_message = {"role": "assistant", "content": answer}
            print_chat_message(ai_message)
            chat_history.append(ai_message)

            # Truncate chat history to keep 20 messages max
            if len(chat_history) > 20:
                chat_history = chat_history[-20:]

            # Update chat history in session state
            st.session_state.chat_history[MODEL] = chat_history

    if __name__ == "__main__":
        main()
else:
    st.error("You do not have access to this page.")