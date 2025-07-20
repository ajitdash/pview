import streamlit as st
import os

# --- Demo Credentials ---
DEMO_USERNAME = "demo"
DEMO_PASSWORD = "password123"
USER_CREDENTIALS = {
    "username": DEMO_USERNAME,
    "password": DEMO_PASSWORD
}

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
    files = [
        f for f in os.listdir(folder_path) 
        if os.path.isfile(os.path.join(folder_path, f))
    ]
    if files:
        selected_file = st.selectbox('Select a file', files)
        return os.path.join(folder_path, selected_file)
    else:
        st.info("No files uploaded yet.")
        return None

# --- Session State ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- Login Screen ---
if not st.session_state.logged_in:
    st.title("PDE Application - Login")
    login_box = st.empty()
    with login_box.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        submitted = st.form_submit_button("Login")
        if submitted:
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.success("Login successful!")
            else:
                st.error("Invalid username or password.")

    st.markdown("""
    <div style="margin-top:16px;padding:10px;border:1px solid #EEE;border-radius:5px;background:#fafafa;">
        <strong>Example credentials:</strong><br>
        <b>Username</b>: <code>demo</code><br>
        <b>Password</b>: <code>password123</code>
    </div>
    """, unsafe_allow_html=True)

# --- Main Application (Tabs) ---
else:
    st.title("PDE Application")

    tab1, tab2 = st.tabs(["📤 File Upload", "📄 Content View"])

    with tab1:
        st.header("File Upload")
        uploaded_file = st.file_uploader("Choose a file to upload")
        if uploaded_file is not None:
            saved_path = save_uploaded_file(uploaded_file)
            st.success(f"File '{uploaded_file.name}' uploaded successfully!")

    with tab2:
        st.header("Content Viewer")
        folder = 'uploaded_files'
        if not os.path.exists(folder) or len(os.listdir(folder)) == 0:
            st.warning("No files found. Please upload a file first.")
        else:
            file_path = file_selector(folder)
            if file_path:
                # Display editable for common text files and preview for images
                file_name = os.path.basename(file_path)
                file_ext = file_name.lower().split('.')[-1]
                if file_ext in ['txt', 'csv', 'json']:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    st.code(content, language="text")
                elif file_ext in ['png', 'jpg', 'jpeg']:
                    st.image(file_path)
                else:
                    st.info(f"Uploaded file: {file_name}")

    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({'logged_in': False}))



# --- Unauthorized access redirect ---
elif not st.session_state.logged_in:
    st.session_state.page = 'login'
    st.experimental_rerun()
