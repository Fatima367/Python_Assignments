import streamlit as st
import hashlib
from cryptography.fernet import Fernet
import json
import os
import time
import base64

STORAGE_FILE = "stored_data.json"
FILE_FOR_KEYS = "fernet_keys.key"
LOCKOUT_DURATION = 600

stored_data = {}

# Load data on app startup
if os.path.exists(STORAGE_FILE):
    with open(STORAGE_FILE, "r") as file:
        stored_data = json.load(file)

def save_data():
    with open(STORAGE_FILE, "w") as file:
        json.dump(stored_data, file)

# Generating a key (it must be stored securely in production)
def load_fernet_key():
    if os.path.exists(FILE_FOR_KEYS):
        with open(FILE_FOR_KEYS, "rb") as file:
            return file.read()
    key = Fernet.generate_key()
    with open(FILE_FOR_KEYS, "wb") as file:
        file.write(key)
    return key

KEY = load_fernet_key()
cipher = Fernet(KEY)

# Data storage in-memory
failed_attempts = 0
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

if "lockout_time" not in st.session_state:
    st.session_state.lockout_time = 0

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# Function to hash passkey
def hash_passkey(passkey):
    hashed = hashlib.pbkdf2_hmac('sha256', passkey.encode(), salt=b"somesalt", iterations=100_000)
    return base64.b64encode(hashed).decode()

# Function to encrypt data
def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

# Function to decrypt data
def decrypt_data(encrypted_text):
    return cipher.decrypt(encrypted_text.encode()).decode()

def is_locked_out():
    if st.session_state.failed_attempts >= 3:
        if time.time() - st.session_state.lockout_time < LOCKOUT_DURATION:
            return True
        st.session_state.failed_attempts = 0
    return False


# UI with Streamlit
st.set_page_config(
    page_title="Secure Data Encryption", 
    page_icon="🔐", 
    layout="centered"
    )
st.title("🔒 Secure Data Encryption System")

if st.session_state.current_user:
    st.success(f"Logged in as: {st.session_state.current_user}")

menu = ["Home", "Store Data", "Retrieve Data", "My Account"]

if st.session_state.current_user:
    menu.append("Logout")

choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Home":
    st.subheader("🏠 Welcome to the Secure Data System")
    st.write("Use this app to **securely store and retrieve data** using unique passkeys.")
    st.write("Go to **My Account** to Login or Signup")

elif choice == "Store Data":
    st.subheader("📂 Store Data Securely")
    if not st.session_state.current_user:
        st.warning("🔐 Please login first.")
        st.stop()
    data_title = st.text_input("Enter Title for the data:")
    user_data = st.text_area("Enter Data:")

    if st.button("Encrypt & Save"):
        if user_data and data_title:
            encrypted_text = encrypt_data(user_data)
            data = {"title": data_title, "data content": encrypted_text}
            user_entries = stored_data[st.session_state.current_user].get("data",[])
            for i, item in enumerate(user_entries):
                if item["title"].lower() == data_title.lower():
                    user_entries[i] = data
                    break
            else:
                user_entries.append(data)
            stored_data[st.session_state.current_user]["data"] = user_entries
            save_data()     
            st.success("✅ Data stored securely!")
        else:
            st.error("⚠️ Both fields are required!")

elif choice == "Retrieve Data":
    st.subheader("🔍 Retrieve Your Data")

    user = st.session_state.current_user
    user_entries = stored_data[user].get("data", [])

    if not user_entries:
        st.warning("ℹ No data stored.")
        st.stop()

    titles = [data["title"] for data in user_entries]
    selected_title = st.selectbox("Choose a Title", titles)

    passkey = st.text_input("Enter Passkey Again:", type="password")

    if st.button("Decrypt"):
        if hash_passkey(passkey) == stored_data[user]["passkey"]:
            st.session_state.failed_attempts = 0
            is_title_matched = next((item for item in user_entries if item["title"] == selected_title), None)

            if is_title_matched:
                decrypted_data = decrypt_data(is_title_matched["data content"])
            else:
                st.warning("❌ Data not found.")

            if decrypted_data:
                st.success(f"✅ Decrypted Data: {decrypted_data}")
            else:
                st.session_state.failed_attempts += 1
                st.error(f"❌ Incorrect passkey! Attempts remaining: {3 - st.session_state.failed_attempts}")

                if st.session_state.failed_attempts >= 3:
                    st.session_state.lockout_time = time.time()
                    st.warning("🚫Too many failed attempts! Redirecting to Login Page.")
                    st.experimental_rerun()
        else:
            st.error("⚠️ Both fields are required!")

elif choice == "My Account":
    st.subheader("👤 My Account")
    is_signed_up = st.checkbox("New user? Register")

    if is_signed_up:
        st.markdown("### SignUp") 
        new_user = st.text_input("Enter a unique username")
        new_password = st.text_input("Passkey", type="password") 

        if st.button("Register"):
            if new_user and new_password:
                if new_user in stored_data:
                    st.warning("⚠ User exists!")
                else:
                    stored_data[new_user] = {"passkey": hash_passkey(new_password), "encrypted_data": ""}
                    save_data()
                    st.success("✅ Signed up successfully!")
            else:
                st.error("⚠ All fields required.")
    else:
        st.markdown("### Login")
        username = st.text_input("Enter your username")
        passkey = st.text_input("Passkey", type="password")

        if st.button("Login"):
            if username in stored_data and hash_passkey(passkey) == stored_data[username]["passkey"]:
                st.session_state.current_user = username
                st.session_state.failed_attempts = 0
                st.success("✅ Login successful!")
            else:
                st.session_state.failed_attempts += 1
                if st.session_state.failed_attempts >= 3:
                    st.session_state.lockout_time = time.time()
                st.error(f"❌ Incorrect passkey! Attempts remaining: {3 - st.session_state.failed_attempts}")


elif choice == "Logout":
    st.session_state.current_user = None
    st.success("👋 Logged out!")
    st.rerun()