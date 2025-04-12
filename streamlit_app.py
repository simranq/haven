import streamlit as st
import requests
import base64
from pathlib import Path

# Page Configuration
st.set_page_config(
    page_title="Haven Authentication",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Set paths for assets
ASSETS_PATH = Path("assets")
BG_IMAGE_PATH = ASSETS_PATH / "b3.jpg"
LOGO_PATH = ASSETS_PATH / "logo.png"

# Function to encode and set background image
def set_bg_image():
    try:
        with open(BG_IMAGE_PATH, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        st.markdown(
            f"""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');
            .stApp {{
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(35px) saturate(200%);
                -webkit-backdrop-filter: blur(35px) saturate(200%);
                background-image: url(data:image/jpeg;base64,{encoded_string});
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                padding: 20px;
            }}

            /* Main Glass Panel Styling */
            .glass-panel {{
                background: rgba(255, 255, 255, 0.3);
                backdrop-filter: blur(35px) saturate(200%);
                -webkit-backdrop-filter: blur(35px) saturate(200%);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.4); /* Highlighted border */
                box-shadow: 0 8px 32px rgba(31, 38, 135, 0.6); /* Strong shadow */
                padding: 40px;
                max-width: 600px;
                margin: 0 auto;
                color: black;
            }}

            /* Form Inputs */
            .stTextInput>div>div>input {{
                font-family: 'Montserrat';
                background: rgba(255, 255, 255, 0.5);
                color: black;
                border-radius: 12px;
                padding: 12px;
                border: 1px solid rgba(255, 255, 255, 0.6); /* Subtle border */
                margin-bottom: 15px;
            }}

            .stTextInput>div>div>input::placeholder {{
                color: black;
                font-family: 'Montserrat';
            }}

            /* Form Buttons */
            .stButton>button {{
                font-family: 'Montserrat'; /* Ensure Montserrat font */
                background: linear-gradient(135deg, rgba(187, 134, 252, 0.9), rgba(124, 77, 255, 0.9));
                color: white;
                border: none;
                border-radius: 12px;
                padding: 10px;
                width: 100%;
                font-weight: bold;
                margin-top: 15px;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }}

            .stButton>button:hover {{
                transform: translateY(-3px);
                box-shadow: 0 8px 20px rgba(124, 77, 255, 0.5);
            }}

            /* Title and Subtitle */
            h2{{
                color: white;
            }}
            .auth-title {{
                font-family: 'Montserrat'; /* Montserrat font for title */
                font-size: 1.5rem;
                font-weight: bold;
                text-align: center;
                margin-bottom: 1rem;
                color: white;
            }}

            .auth-subtitle {{
                font-family: 'Montserrat'; /* Montserrat font for subtitle */
                text-align: center;
                color: white;
                margin-bottom: 20px;
            }}

            /* Logo Styling */
            .logo-container {{
                text-align: center;
                margin-bottom: 30px;
                position:sticky;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error("Background image not found in assets folder")

# Set the background
set_bg_image()

# FastAPI backend URL
BACKEND_URL = "http://localhost:8000"

# Session State
if "token" not in st.session_state:
    st.session_state.token = None

# Main Auth Component
def auth_component():
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try:
        st.image(str(LOGO_PATH), width=150)
    except FileNotFoundError:
        st.markdown('<h1 style="color: black;">HAVEN</h1>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tabs for Login and Signup
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.markdown('<h2 class="auth-title">Welcome Back</h2>', unsafe_allow_html=True)
        st.markdown('<p class="auth-subtitle">Sign in to access your dashboard</p>', unsafe_allow_html=True)
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            if st.form_submit_button("Login"):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/token",
                        data={"username": email, "password": password}
                    )
                    if response.status_code == 200:
                        st.session_state.token = response.json()["access_token"]
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to backend")
    
    with tab2:
        st.markdown('<h2 class="auth-title">Create Account</h2>', unsafe_allow_html=True)
        st.markdown('<p class="auth-subtitle">Join our secure community</p>', unsafe_allow_html=True)
        with st.form("register_form"):
            new_email = st.text_input("Email", placeholder="Enter your email", key="reg_email")
            new_password = st.text_input("Password", type="password", placeholder="Enter your password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            new_name = st.text_input("Full Name", placeholder="Your name", key="reg_name")
            new_age = st.number_input("Age", min_value=1, max_value=120, key="reg_age")
            if st.form_submit_button("Sign Up"):
                if new_password != confirm_password:
                    st.error("Passwords don't match")
                else:
                    try:
                        response = requests.post(
                            f"{BACKEND_URL}/register",
                            json={
                                "email": new_email,
                                "password": new_password,
                                "name": new_name,
                                "age": new_age
                            }
                        )
                        if response.status_code == 200:
                            st.success("Registration successful! Please login.")
                            st.rerun()
                        else:
                            st.error(response.json().get("detail", "Registration failed"))
                    except requests.exceptions.ConnectionError:
                        st.error("Backend service unavailable")
    st.markdown('</div>', unsafe_allow_html=True)  # Close glass-panel

# Main App
def main():
    auth_component()

if __name__ == "__main__":
    if st.session_state.token:
        st.success("You are already logged in!")
        if st.button("Logout"):
            st.session_state.token = None
            st.rerun()
    else:
        main()