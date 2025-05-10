import os 
import streamlit as st
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from instruction import instruction_for_gemini
from streamlit_option_menu import option_menu
import hashlib
import base64
import random
import json
import datetime
from fpdf import FPDF
from css_style import load_css
import time
import asyncio

USERS_STORAGE_FILE = "users.json"
NOTES_STORAGE_FILE =  "notes.json"
LOCKOUT_DURATION = 500


# Loading user data -----------------------------------------------------------------------
stored_data = {}
total_notes:list = []

if os.path.exists(USERS_STORAGE_FILE):
    with open(USERS_STORAGE_FILE, "r") as file:
        stored_data = json.load(file)

def save_user_data():
    with open(USERS_STORAGE_FILE, "w") as file:
        json.dump(stored_data, file)


if os.path.exists(NOTES_STORAGE_FILE):
    with open(NOTES_STORAGE_FILE, "r") as file:
        total_notes = json.load(file)

def save_notes():
    with open(NOTES_STORAGE_FILE, "w") as file:
        json.dump(total_notes, file)


# CLASSES
# Login------------------------------------------------------------------------------------------------------

class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.message = ""
        self.success = False

        for user_id, user_data in stored_data.items():
            if user_data.get("username") == username and verify_password(password, user_data.get("password")):
                st.session_state.is_logged_in = True
                st.session_state.user = username
                st.session_state.user_id = user_id
                self.message = "Login succesful"
                self.success = True
                return 
        
        self.message = "Invalid username or password"

# Signup--------------------------------------------------------------------------------------------------

class RegisterUser:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.message = ""
        self.success = False

        for user in stored_data.values():
            if user.get("username") == self.username:
                self.message =  "Username already exists"
                return

        if len(password) < 6:
            self.message = "Password must be at least 6 characters long"
            return
        
        user_id = str(len(stored_data) + 1)
        stored_data[user_id] = {
            "username" : self.username,
            "password" : hash_password(self.password)
        }

        save_user_data()
        self.message = "Registration succesful"
        self.success = True

# Logout-----------------------------------------------------------------------------------------------------
class Logout:
    def __init__(self):
        st.session_state.is_logged_in = False
        st.session_state.user = None
        st.session_state.user_id = None
        st.message = "Logged out succesfully"
        st.session_state.current_page = "home"


# Notes-------------------------------------------------------------------------------------
note_colors = [
    "#D3E4ED",  # Soft Blue
    "#E3F4F1",  # Pale Mint
    "#F5E1DC",  # Light Peach
    "#D1E8E2",  # Light Teal
    "#F7D8BA",  # Warm Beige
    "#E8D1B0",  # Soft Tan
    "#F2D7D5",  # Light Pink
    "#B4C8B3",  # Pale Sage Green
]

class Notes:
    @staticmethod
    def create_note(title, content, about, type="note", starred=False):
        global total_notes

        color = random.choice(st.session_state.note_colors)
        note = {
            "id": len(total_notes) + 1,
            "title": title,
            "content": content,
            "about": about,
            "user_id": st.session_state.user_id,
            "type" : type,
            "starred": starred,
            "color": color,
            "created_at" : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        total_notes.append(note)
        save_notes()
        return note

    @staticmethod
    def get_user_notes(note_type = None):
        global total_notes

        if note_type:
            user_notes = [note for note in total_notes if note.get("user_id") == st.session_state.user_id and note.get("type") == note_type]
        else:
            user_notes = [note for note in total_notes if note.get("user_id") == st.session_state.user_id]

        # for sorting the starred notes
        starred_notes = [note for note in total_notes if note.get("user_id") == st.session_state.user_id and note.get("starred", False)]
        regular_notes = [note for note in total_notes if not note.get("starred", False) and note.get("user_id") == st.session_state.user_id]

        return starred_notes + regular_notes

    @staticmethod
    def delete_note(note_id):
        global total_notes
        for i, note in enumerate(total_notes):
            if note_id == note.get("id") and note.get("user_id") == st.session_state.user_id:
                del total_notes[i]
                break
        
        save_notes()

    @staticmethod
    def update_note(note_id, title, content, about, starred=None):
        global total_notes

        for note in total_notes:
            if note_id == note.get("id") and note.get("user_id") == st.session_state.user_id:
                note["title"] = title
                note["content"] = content
                note["about"] = about
                note["starred"] = starred
                break

        save_notes()

    @staticmethod
    def is_starred(note_id):
        global total_notes

        for note in total_notes:
            if note_id == note.get("id") and note.get("user_id") == st.session_state.user_id:
                note["starred"] = not note.get("starred")
                break
        
        save_notes()

    @staticmethod
    def get_note(note_id):
        global total_notes
        for note in total_notes:
            if note_id == note.get("id") and note.get("user_id") == st.session_state.user_id:
                return note
        return None
    
# Password encryption ---------------------------------------------------------------------------
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

#---------------------------------------------------------------------------------------------------------
    
def generate_pdf(title, content, category= None):
    pdf = FPDF()
    pdf.add_page()
    
    # Set up the PDF
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, title, ln=True, align="C")
    
    if category:
        pdf.set_font("Arial", "I", 12)
        pdf.cell(0, 10, f"Category: {category}", ln=True)
    
    pdf.ln(5)
    
    # Add content
    pdf.set_font("Arial", "", 12)
    
    # Split content into lines to avoid text going off the page
    if not isinstance(content, list):
        lines = content.split('\n')
    else:
        lines = content

    for line in lines:
        # Handle long lines by wrapping
        while len(line) > 80:  # Approximate characters per line
            pdf.multi_cell(0, 10, line[:80])
            line = line[80:]
        pdf.multi_cell(0, 10, line)
    
    # Return PDF as bytes
    return pdf.output(dest="S").encode("latin1")


# Generating cheat codes with AI-----------------------------------------------------------------
def generate_cheat_code(category, query):
    load_dotenv()

    gemini_api_key = os.getenv("GOOGLE_API_KEY")
    
    try:
        if not gemini_api_key:
            return "Error: Google API Key not found. Please add it to your .env file."

        provider = AsyncOpenAI(
            api_key = gemini_api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai"
        )

        model = OpenAIChatCompletionsModel(
            model = "gemini-2.0-flash",
            openai_client = provider
        )

        agent = Agent(
            name = "Cheat Codes Generator",
            instructions = instruction_for_gemini,
            model = model
            )

        full_query = f"{category} cheat code for: {query}"


        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(Runner.run(agent, full_query))
        loop.close()

        # adding chat to history
        st.session_state.chat_history = [
            {"role": "user", "content": full_query},
            {"role": "assistant", "content": result.final_output}
        ]

        return result.final_output
    
    except Exception as e:
        return f"Error generating cheat code: {str(e)}"


# Initializing data in streamlit session state----------------------------------------------------------------
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

if "cheat_code_category" not in st.session_state:
    st.session_state.cheat_code_category  = None
    
if "cheat_code_result" not in st.session_state:
    st.session_state.cheat_code_result  = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if 'note_colors' not in st.session_state:
    st.session_state.note_colors = ["#fff9c4", "#c8e6c9", "#bbdefb", "#f8bbd0", "#e1bee7"]

# UI components----------------------------------------------------------------------------------------------
def header():
    col1, col2, col3 = st.columns([5,1,1])

    with col1:
        st.title("📝 NotesApp")

    with col2:
        if st.session_state.is_logged_in:
            if st.button("Home", key="home_btn"):
                st.session_state.current_page = "home"
                st.rerun()
    with col3:
        if st.session_state.is_logged_in:
            if st.button("Logout", key="logout_btn"):
                Logout()
                st.rerun()

        else:
            if st.button("Login", key="login_btn"):
                st.session_state.current_page = 'login'
                st.rerun()

def footer():
    st.markdown("""
        <div style="text-align: center; margin-top: 3rem; padding: 1rem; background-color: #f8f9fa; border-radius: 10px;">
            <p>Made by Fatima Faisal with ❤️ for learning and growth</p>
        </div>
    """, unsafe_allow_html=True)

def sidebar():
    if st.session_state.is_logged_in:
        with st.sidebar:
            st.markdown(f"### Welcome, {st.session_state.user}!")

            if st.button("🏠 Home", key="sidebar_home"):
                st.session_state.current_page = "home"
                st.rerun()

            if st.button("📝 My Notes", key="sidebar_notes"):
                st.session_state.current_page = "my_notes"
                st.rerun()

            if st.button("🔍 Cheat Codes", key="sidebar_cheat_codes"):
                # Reset cheat code step when navigating to cheat codes
                st.session_state.cheat_code_step = 1
                st.session_state.cheat_code_category = None
                st.session_state.cheat_code_result = None
                st.session_state.cheat_code_query = None
                st.session_state.chat_history = []
                st.session_state.current_page = 'cheat_codes'
                st.rerun()

def home():
    st.markdown("<div class='hero-container'>", unsafe_allow_html=True)
    st.markdown("<h1>Welcome to NotesApp</h1>", unsafe_allow_html=True)
    st.markdown("<p>Your personal space for notes and cheat codes</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div style='background-color: white; border-radius: 10px; padding: 20px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <div style='font-size: 48px; color: #3498db;'>
                    ➕
                </div>
                <h3>Create Note</h3>
            </div>
            """, 
            unsafe_allow_html=True
        )
        if st.button("Create Note", key="create_note_btn"):
            st.session_state.current_page = "create_note"
            st.rerun()

    with col2:
        st.markdown(
            """
            <div style='background-color: white; border-radius: 10px; padding: 20px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <div style='font-size: 48px; color: #3498db;'>
                    🔍
                </div>
                <h3>Get Cheat Codes</h3>
            </div>
            """, 
            unsafe_allow_html=True
        )
        if st.button("Get Cheat Codes", key="get_cheat_codes_btn"):
            # Reset cheat code step when navigating to cheat codes
            st.session_state.cheat_code_step = 1
            st.session_state.cheat_code_category = None
            st.session_state.cheat_code_result = None
            st.session_state.cheat_code_query = None
            st.session_state.chat_history = []
            st.session_state.current_page = 'cheat_codes'
            st.rerun()

def login_page():
    st.markdown("<h2 style='text-align: center;'>Login</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("password", type="password")
            submit = st.form_submit_button("Login")
            if submit:
                login = Login(username, password)
            

            if submit:
                if login.success:
                    st.success(login.message)
                    time.sleep(1)
                    st.session_state.current_page = 'home'
                    st.rerun()
                else:
                    st.error(login.message)
        
        st.markdown("Don't have an account?")
        if st.button("Register", key="register_btn"):
            st.session_state.current_page = "register"
            st.rerun()
            
        if st.button("Back to Home", key="back_home_btn"):
            st.session_state.current_page = 'home'
            st.rerun()

def register_page():
    st.markdown("<h2 style='text-align: center;'>Register</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        with st.form("register_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Register")
            register = RegisterUser(username, password)

            if submit:
                if register.success:
                    st.success(register.message)
                    time.sleep(1)
                    st.session_state.current_page = "home"
                    st.rerun()
                else:
                    st.error(register.message)
        st.markdown("Already have an account?")
        if st.button("Login", key="login_from_register"):
            st.session_state.current_page = "login"
            st.rerun()

        if st.button("← Back",  key="back_from_create"):
            st.session_state.current_page = "home"
            st.rerun()

def create_note_page():
    st.markdown("<h2>Create Note</h2>", unsafe_allow_html=True)

    if st.button("← Back", key="back_from_create"):
        st.session_state.current_page = "home"
        st.rerun()

    with st.form("create_note_form"):
        title = st.text_input("Title")
        about = st.text_input("About Tag")
        content = st.text_area("Content", height=100)
        submit = st.form_submit_button("Save Note")

        if submit:
            if title and content:
                Notes.create_note(title, content, about)
                st.success("Note created successfully!")
                time.sleep(1)
                st.session_state.current_page =  "my_notes"
                st.rerun()
            else:
                st.error("Title and content are required")

def my_notes_page():
    st.markdown("<h2>My Notes</h2>", unsafe_allow_html=True)

    if st.button("+ Create New Note", key="create_from_my_notes"):
        st.session_state.current_page = "create_note"
        st.rerun()
    

    notes = Notes.get_user_notes(note_type="note")

    if not notes:
        st.info("You don't have any notes yet. Create your first note!")
    else:
        cols = st.columns(3)
        for i, note in enumerate(notes):
            with cols[i % 3]:
                color = note.get("color", "#fff9c4")
                starred = "⭐" if note.get("starred") else ""

                note_key = f"note_{note["id"]}"

                st.markdown(
                    f"""
                    <div class='note-card' style='background-color: {color};'>
                        <h3>{starred}{note['title']}</h3>
                        <p style='color: #666; font-size: 0.8rem;'>{note['about']}</p>
                        <p>{note['content'][:20]}{'...' if len(note['content']) > 20 else ''}</p>
                        <p style='color: #999; font-size: 0.7rem; text-align: right;'>{note['created_at']}</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    if st.button("📜", key=f"view_{note['id']}"):
                        st.session_state.note_id = note["id"]
                        st.session_state.current_page = "view_note"
                        st.rerun()
                with col2:
                    if st.button("✏️", key=f"edit_{note['id']}"):
                        st.session_state.note_id = note['id']
                        st.session_state.current_page = 'edit_note'
                        st.rerun()
                         
                
                with col3:
                    star_icon = "⭐" if note.get("starred") else "☆"
                    if st.button(star_icon, key=f"star_{note['id']}"):
                        Notes.is_starred(note['id'])
                        st.rerun()
                         
                
                with col4:
                    if st.button("🗑️", key=f"delete_{note['id']}"):
                        Notes.delete_note(note['id'])
                        st.rerun()

def cheat_codes_list():
    st.markdown("<h2>My Cheat Codes</h2>", unsafe_allow_html=True)

    if st.button("Find New Cheat Codes", key="find_new_cheat_codes"):
        st.session_state.cheat_code_step = 1
        st.session_state.cheat_code_category = None
        st.session_state.cheat_code_result = None
        st.session_state.cheat_code_query = None
        st.session_state.chat_history = []
        st.session_state.current_page = 'cheat_codes'

        cheat_codes = Notes.get_user_notes(note_type="cheat_code")

        st.rerun()

        if not cheat_codes:
            st.info("You don't have any saved cheat codes yet. Find some now!")
    else:
        # Display cheat codes in a grid
        cols = st.columns(3)
        for i, code in enumerate(cheat_codes):
            with cols[i % 3]:
                color = code.get('color', '#bbdefb')
                starred = "⭐ " if code.get('starred', False) else ""
                
                st.markdown(
                    f"""
                    <div style='background-color: {color}; border-radius: 10px; padding: 15px; margin-bottom: 15px;'>
                        <h3>{starred}{code['title']}</h3>
                        <p style='color: #666; font-size: 0.8rem;'>{code['about']}</p>
                        <p>{code['content'][:100]}{'...' if len(code['content']) > 100 else ''}</p>
                        <p style='color: #999; font-size: 0.7rem; text-align: right;'>{code['created_at']}</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Create a row of buttons for each cheat code
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("📜", key=f"view_{code['id']}"):
                        st.session_state.note_id = code['id']
                        st.session_state.current_page = 'view_note'
                        st.rerun()
                
                with col2:
                    if st.button("✏️", key=f"edit_{code['id']}"):
                        st.session_state.note_id = code['id']
                        st.session_state.current_page = 'edit_note'
                        st.rerun()
                                         
                with col3:
                    star_icon = "⭐" if code.get('starred', False) else "☆"
                    if st.button(star_icon, key=f"star_{code['id']}"):
                        Notes.is_starred(code['id'])
                        st.rerun()
                
                with col4:
                    if st.button("🗑️", key=f"delete_{code['id']}"):
                        Notes.delete_note(code['id']) 
                        st.rerun()  

def view_note():
    note = Notes.get_note(st.session_state.note_id)

    if not note:
        st.error("Note not found")
        st.session_state.current_page = 'my_notes'
        st.rerun()
         
    
    st.markdown(f"<h2>{note['title']}</h2>", unsafe_allow_html=True)

    if st.button("← Back", key="back_from_view"):
        if note['type'] == 'cheat_code':
            st.session_state.current_page = 'cheat_codes_list'
            st.rerun()
        else:
            st.session_state.current_page = 'my_notes'
            st.rerun()

    color = note.get('color', '#fff9c4')
    starred = "⭐ " if note.get('starred', False) else ""
    
    st.markdown(
        f"""
        <div style='background-color: {color}; border-radius: 10px; padding: 20px; margin-bottom: 20px;'>
            <p style='color: #666; font-size: 0.9rem;'><strong>About:</strong> {note['about']}</p>
            <div style='white-space: pre-line; margin: 20px 0;'>{note['content']}</div>
            <p style='color: #999; font-size: 0.8rem; text-align: right;'>{note['created_at']}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("✏️ Edit", key="edit_from_view"):
            st.session_state.current_page = 'edit_note'
            st.rerun()
             
    
    with col2:
        star_text = "⭐ Unstar" if note.get('starred', False) else "☆ Star"
        if st.button(star_text, key="star_from_view"):
            Notes.is_starred(note['id'])
            st.rerun()
             
    
    with col3:
        if st.button("🗑️ Delete", key="delete_from_view"):
            Notes.delete_note(note['id'])
            if note['type'] == 'cheat_code':
                st.session_state.current_page = 'cheat_codes_list'
                st.rerun()
            else:
                st.session_state.current_page = 'my_notes'
                st.rerun()
             
    
    with col4:
        if note['type'] == 'cheat_code':
            # Generate PDF for download
            pdf_bytes = generate_pdf(note['title'], note['content'], note['about'])
            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name=f"{note['title'].replace(' ', '_').lower()}.pdf",
                mime="application/pdf",
                key="download_pdf"
            )

def edit_note():
    note = Notes.get_note(st.session_state.note_id)

    if not note:
        st.error("Note not found")
        st.session_state.current_page = 'my_notes'
        st.rerun()

    st.markdown(f"<h2>Edit Note</h2>", unsafe_allow_html=True)

    if st.button("← Back", key="back_from_edit"):
        st.session_state.current_page = "view_note"
        st.rerun()

    with st.form("edit_note_form"):
        title = st.text_input("Title", value=note.get("title"))
        about = st.text_input("About Tag", value=note.get("about"))
        content = st.text_area("Content", value=note.get("content"), height=100)
        submit = st.form_submit_button("Save Changes")

        if submit:
            if title and content:
                Notes.update_note(note["id"], title, content, about)
                st.success("Note updated successfully!")
                time.sleep(1)
                st.session_state.current_page = "view_note"
                st.rerun()
            
            else:
                st.error("Title and content are required")

def chat_interface():
    # Displaying chat history
    for message in st.session_state.chat_history:
        role_class = "user" if message["role"] == "user" else "assistant"
        role_label = "You" if message["role"] == "user" else "assistant"

        st.markdown(
            f"""
            <div class="chat-message {role_class}">
                <div><strong>{role_label}</strong></div>
                <div class="content">{message["content"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # chat input 
        # with st.form("chat_form"):
        #     user_input = st.text_area("Your message:", key="user_message", height=100)
        #     submit = st.form_submit_button("Send")

def render_cheat_codes():
    st.markdown("<h2>Find Cheat Codes</h2>", unsafe_allow_html=True)

    if st.button("← Back", key="back_from_cheat_codes"):
        st.session_state.current_page = "home"
        st.rerun()

    # Step 1: select a category section
    if st.session_state.cheat_code_step == 1:
        st.subheader("What type of cheat code are you looking for?")

        # displaying category options
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                """
                <div class='category-card' id='math-card'>
                    <div style='font-size: 36px;'>🧮</div>
                    <h3>Math</h3>
                    <p>Formulas, equations, and calculations</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            if st.button("Select Math", key="select_math"):
                st.session_state.cheat_code_category = "Math"
                st.session_state.cheat_code_step = 2
                st.rerun()

        with col2: 
            st.markdown(
                """
                <div class='category-card' id='code-card'>
                    <div style='font-size: 36px;'>💻</div>
                    <h3>Code</h3>
                    <p>Programming syntax, functions, and snippets</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            if st.button("Select Code", key="select_code"):
                st.session_state.cheat_code_category = "Code"
                st.session_state.cheat_code_step = 2
                st.rerun()

        with col3:
            st.markdown(
                """
                <div class='category-card' id='game-card'>
                    <div style='font-size: 36px;'>🎮</div>
                    <h3>Game</h3>
                    <p>Game strategies, controls, and shortcuts</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            if st.button("Select Game", key="select_game"):
                st.session_state.cheat_code_category = "Game"
                st.session_state.cheat_code_step = 2
                st.rerun()

        # Second row of categories
        col4, col5, col6 = st.columns(3)

        with col4:
            st.markdown(
                """
                <div class='category-card' id='science-card'>
                    <div style='font-size: 36px;'>🔬</div>
                    <h3>Science</h3>
                    <p>Scientific principles, formulas, and concepts</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            if st.button("Select Science", key="select_science"):
                st.session_state.cheat_code_category = "Science"
                st.session_state.cheat_code_step = 2
                st.rerun()
        
        with col5:
            st.markdown(
                """
                <div class='category-card' id='language-card'>
                    <div style='font-size: 36px;'>🗣️</div>
                    <h3>Language</h3>
                    <p>Grammar rules, vocabulary, and expressions</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            if st.button("Select Language", key="select_language"):
                st.session_state.cheat_code_category = "Language"
                st.session_state.cheat_code_step = 2
                st.rerun()
        
        with col6:
            st.markdown(
                """
                <div class='category-card' id='other-card'>
                    <div style='font-size: 36px;'>🔍</div>
                    <h3>Other</h3>
                    <p>Any other type of cheat code</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            if st.button("Select Other", key="select_other"):
                st.session_state.cheat_code_category = "Other"
                st.session_state.cheat_code_step = 2
                st.rerun()

    # second step: Enter query
    elif st.session_state.cheat_code_step == 2:
        st.subheader(f"What {st.session_state.cheat_code_category} cheat code are you looking for?")

        # examples based on category
        if st.session_state.cheat_code_category == "Math":
            st.markdown("Examples: Pythagorean theorem, derivative rules, integration formulas")
        elif st.session_state.cheat_code_category == "Code":
            st.markdown("Examples: Python list comprehension, JavaScript promises, CSS flexbox")
        elif st.session_state.cheat_code_category == "Game":
            st.markdown("Examples: Minecraft crafting recipes, GTA cheat codes, Chess openings")
        elif st.session_state.cheat_code_category == "Science":
            st.markdown("Examples: Periodic table elements, Newton's laws, chemical reactions")
        elif st.session_state.cheat_code_category == "Language":
            st.markdown("Examples: Spanish conjugation, English irregular verbs, French phrases")
        else:
            st.markdown("Examples: Keyboard shortcuts, cooking measurements, gardening tips")


        # input form for specific query:
        # st.form("cheat_code_form"):
        query = st.text_input("Enter your specific query:")
        # submit = st.form_submit_button("Generate Cheat Code")

        if st.button("Generate Cheat Code") and query:
                cheat_code = generate_cheat_code(st.session_state.cheat_code_category, query)

                st.session_state.cheat_code_result = cheat_code
                st.session_state.cheat_code_query = query
                st.session_state.cheat_code_step = 3
                st.rerun()

        if st.button("← Back to Categories", key="back_to_categories"):
            st.session_state.cheat_code_step = 1
            st.session_state.cheat_code_category = None
            st.rerun()

    # Displaying results with options
    elif st.session_state.cheat_code_step == 3:
        st.subheader(f"Cheat Code for: {st.session_state.cheat_code_query}")

        st.markdown("<div class='cheat-code-container'>", unsafe_allow_html=True)
        st.code(st.session_state.cheat_code_result)
        st.markdown("</div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📋 Copy to Clipboard", key="copy_result"):
                st.success("Copied to clipboard!")

        with col2:
            pdf_bytes = generate_pdf(
                f"Cheat Code: {st.session_state.cheat_code_query}", 
                st.session_state.cheat_code_result, 
                st.session_state.cheat_code_category
            )
            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name=f"cheat_code_{st.session_state.cheat_code_query.replace(' ', '_').lower()}.pdf",
                mime="application/pdf",
                key="download_result"
            )

        with col3:
            if st.button("💾 Save as Note", key="save_result"):
                title = f"Cheat Code: {st.session_state.cheat_code_query}"
                about = f"{st.session_state.cheat_code_category} Cheat Code"
                Notes.create_note(title, st.session_state.cheat_code_result, about, type="cheat_code")
                st.success("Cheat code saved successfully!")
                time.sleep(1)
                st.session_state.current_page = 'cheat_codes_list'
                st.rerun()


             # New search button
        if st.button("🔍 New Search", key="new_search"):
            st.session_state.cheat_code_step = 1
            st.session_state.cheat_code_category = None
            st.session_state.cheat_code_result = None
            st.session_state.cheat_code_query = None
            st.session_state.chat_history = []
             
        
        # Chat interface for continuing the conversation
        st.markdown("---")
        st.subheader("Continue the conversation")
        st.markdown("Ask for improvements, clarifications, or additional information about this cheat code.")

        chat_interface()

def main():
    load_css()
    
    header()
    
    sidebar()

    if not st.session_state.is_logged_in and st.session_state.current_page not in ["login", "register", "home"]:
        st.warning("Please login to access this feature")
        st.session_state.current_page = "login"
        st.rerun()

    if st.session_state.current_page == "home":
        home()
    elif st.session_state.current_page == "login":
        login_page()
    elif st.session_state.current_page == "register":
        register_page()
    elif st.session_state.current_page == 'create_note':
        create_note_page()
    elif st.session_state.current_page == 'my_notes':
        my_notes_page()
    elif st.session_state.current_page == 'cheat_codes_list':
        cheat_codes_list()
    elif st.session_state.current_page == 'view_note':
        view_note()
    elif st.session_state.current_page == 'edit_note':
        edit_note()
    elif st.session_state.current_page == 'cheat_codes':
        render_cheat_codes()

    footer()

if __name__ == "__main__":
    main()