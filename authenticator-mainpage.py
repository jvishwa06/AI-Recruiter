import streamlit as st

def authenticate_user(username, password):
    users = {
        'candidate': {'password': 'candi123', 'role': 'employee'},
        'hr': {'password': 'hr123', 'role': 'hr'}
    }
    
    user = users.get(username)
    if user and user['password'] == password:
        return user['role']
    else:
        return None

if 'user_role' not in st.session_state:
    st.session_state.user_role = None

def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        user_role = authenticate_user(username, password)
        if user_role:
            st.session_state.user_role = user_role
            st.success(f"Logged in as {user_role}")
            
            st.query_params["logged_in"] = "true"
        else:
            st.error("Invalid username or password")

def sidebar():
    st.sidebar.title("Navigation")
    
    if st.session_state.user_role == 'employee':
        with st.sidebar.expander("Employee Access", expanded=True):
            st.sidebar.write("You have access to all candidate pages.")

    elif st.session_state.user_role == 'hr':
        with st.sidebar.expander("HR Access", expanded=True):
            st.sidebar.write("You can access all hr pages:")

    else:
        st.sidebar.write("Please log in to access the pages.")

if st.session_state.user_role is None:
    login() 
else:
    sidebar() 