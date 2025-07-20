import streamlit as st
import os

# --- Basic hardcoded user credentials (for demo purposes) ---
USER_CREDENTIALS = {
    "username": "demo",
    "password": "password123"
}

# --- Helper functions ---
def authenticate(username, password):
    return username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']

def save_uploaded_file(uploaded_file, save_dir='uploaded_files'):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_path = os.path.join(save_dir, uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def file_selector(folder_path='uploaded_files'):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    selected_file = st.selectbox('Select a file', files)
    return os.path.join(folder_path, selected_file)

# --- Streamlit App Screen Manager ---
if 'page' not in st.session_state:
    st.session_state.page = 'login'

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- Login Screen ---
if st.session_state.page == 'login':
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.session_state.page = 'upload'
            st.success("Login successful!")
        else:
            st.error("Invalid username or password.")

# --- File Upload Screen ---
elif st.session_state.page == 'upload' and st.session_state.logged_in:
    st.title("File Upload")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        saved_path = save_uploaded_file(uploaded_file)
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
    if st.button("View Uploaded Files"):
        st.session_state.page = 'view'
    st.button("Logout", on_click=lambda: (st.session_state.update({'logged_in': False, 'page':'login'})))

# --- Content Viewer Screen ---
elif st.session_state.page == 'view' and st.session_state.logged_in:
    st.title("File Content Viewer")
    folder = 'uploaded_files'
    if not os.path.exists(folder) or len(os.listdir(folder)) == 0:
        st.warning("No files found. Please upload a file first.")
    else:
        file_path = file_selector(folder)
        # Display file content (supports txt/csv/json, previews images)
        if file_path.endswith(('.txt', '.csv', '.json')):
            with open(file_path, "r", encoding="utf-8") as f:
                st.code(f.read())
        elif file_path.endswith(('.png', '.jpg', '.jpeg')):
            st.image(file_path)
        else:
            st.info(f"Uploaded file: {file_path.split(os.sep)[-1]}")
    if st.button("Back to Upload"):
        st.session_state.page = 'upload'
    st.button("Logout", on_click=lambda: (st.session_state.update({'logged_in': False, 'page':'login'})))

# --- Unauthorized access redirect ---
elif not st.session_state.logged_in:
    st.session_state.page = 'login'
    st.experimental_rerun()
