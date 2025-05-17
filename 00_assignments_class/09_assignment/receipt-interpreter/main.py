from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import asyncio
import hashlib
import base64
import json
import csv
import os

st.set_page_config(
    page_title="AI Receipt Interpreter",
    page_icon="📜",
    layout="wide"
)

USERS_STORAGE_FILE = "users.json"
LOCKOUT_DURATION = 500


# ========================================= Loading user data =====================================================================
stored_user_data = {}

if os.path.exists(USERS_STORAGE_FILE):
    with open(USERS_STORAGE_FILE, "r") as file:
        stored_data = json.load(file)

def save_user_data():
    with open(USERS_STORAGE_FILE, "w") as file:
        json.dump(stored_data, file)

# ======================================== Password encryption =========================================================
def hash_password(password):
    salt = os.urandom(16) # Random secure salt
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return base64.b64encode(salt + hashed).decode()

def verify_password(password, stored_value):
    decoded = base64.b64decode(stored_value.encode())
    salt = decoded[:16]
    stored_hash = decoded[16:] 
    new_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt ,100_000)
    return new_hash == stored_hash  


failed_attempts = 0

def is_locked_out():
    return st.session_state.get("failed_attempts", 0) >= 3


# =============================================== CLASSES ===================================================
# =============================================== Login ======================================================

class Login:
    def __init__(self, username, password, email= None):
        self.username = username
        self.email = email | None
        self.password = password
        self.message = ""
        self.success = False

        for user_id, user_data in stored_user_data.items():
            if user_data.get("username") == username or user_data.get("email") == email and verify_password(password, user_data.get("password")):
                st.session_state.is_logged_in = True
                st.session_state.user = username
                st.session_state.user_id = user_id
                self.message = "Login succesful"
                self.success = True
                return 
        
        self.message = "Invalid username or password"

# ============================================= Signup =========================================================

class RegisterUser:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.message = ""
        self.success = False

        if '.com' and '@' not in self.email:
            self.message = "Please enter a valid email address"
            return

        for email in stored_user_data.values():
            if email.get("email") == self.email:
                self.message = "This email is already registered"
                return    

        for user in stored_user_data.values():
            if user.get("username") == self.username:
                self.message =  "Username already exists"
                return

        if len(password) < 6:
            self.message = "Password must be at least 6 characters long"
            return
        
        user_id = str(len(stored_user_data) + 1)
        stored_user_data[user_id] = {
            "username" : self.username,
            "password" : hash_password(self.password)
        }

        save_user_data()
        self.message = "Registration successful"
        self.success = True

# ============================================== Logout ===========================================================
class Logout:
    def __init__(self):
        st.session_state.is_logged_in = False
        st.session_state.user = None
        st.session_state.user_id = None
        st.message = "Logged out succesfully"
        st.session_state.current_page = "home"


# ============================================ AI Receipt Intrepreter =============================================
def interpret_receipt(user_input):
    
    load_dotenv()

    gemini_api_key = os.getenv("GOOGLE_API_KEY")

    if not gemini_api_key:
        return "Error: Google API Key not found. Please add it to your .env file."
    
    provider = AsyncOpenAI(
        api_key= gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    )

    model = OpenAIChatCompletionsModel(
        model= "gemini-2.0-flash",
        openai_client= provider
    )

    agent = Agent(
        name = "AI Receipt Interpreter",
        instructions= """
            When the user uploads a photo of a receipt, extract the following information:

            1. Merchant name
            2. List of purchased items (with quantities and prices, if available)
            3. Total amount

            Then:
            4. Identify and tag the expense category (e.g., Meals, Travel, Office Supplies)
            5. Generate a structured expense report containing all extracted and categorized information.
            """ ,
        model= model
    )

    image = Image.open(user_input)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(Runner.run(agent, image))
    loop.close()

    return result.final_output
