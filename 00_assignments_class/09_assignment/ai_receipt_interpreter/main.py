import google.generativeai as genai
from css_style import custom_css
from dotenv import load_dotenv
from datetime import datetime
import streamlit as st
from PIL import Image
import hashlib
import base64
import json
import time
import os
import re

st.set_page_config(
    page_title="AI Receipt Interpreter",
    page_icon="🧾",
    layout="wide"
)

custom_css()

USERS_STORAGE_FILE = "users.json"
RECEIPTS_STORAGE_FILE = "receipts.json"
FREE_RECEIPT_LIMIT = 5
LOCKOUT_DURATION = 500

# ======================================== LOADING DATA ===================================================

stored_users_data = {}
stored_receipts_data = {}

if os.path.exists(USERS_STORAGE_FILE):
    with open(USERS_STORAGE_FILE, "r") as file:
        stored_users_data = json.load(file)

if os.path.exists(RECEIPTS_STORAGE_FILE):
    with open(RECEIPTS_STORAGE_FILE, "r") as file:
        stored_receipts_data = json.load(file)

def save_user_data():
    with open(USERS_STORAGE_FILE, "w") as file:
        json.dump(stored_users_data, file)

def save_receipt_data():
    with open(RECEIPTS_STORAGE_FILE, "w") as file:
        json.dump(stored_receipts_data, file)

# =========================================== PASSWORD ENCRYPTION ==========================================

def hash_password(password):
    salt = os.urandom(16)   # random secure salt
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return base64.b64encode( salt + hashed ).decode()

def verify_password(password, stored_value):
    decoded = base64.b64decode(stored_value.encode())
    salt = decoded[:16]
    stored_hash = decoded[16:]
    new_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return new_hash == stored_hash


failed_attempts = 0

def is_locked_out():
    return st.session_state.get("failed_attempts", 0) >= 3

# ================================================ CLASSES ===================================================
# ================================================ LOGIN =====================================================

class Login:
    def __init__(self, username, password, email=None):
        self.username = username
        self.email = email or None
        self.password = password
        self.message = ""
        self.success = False

        for user_id, user_data in stored_users_data.items():
            if (user_data.get("username") == username or user_data.get("email") == email) and verify_password(password, user_data.get("password")):
                st.session_state.is_logged_in = True
                st.session_state.user = username
                st.session_state.user_id = user_id
                self.message = "Login successful"
                self.success = True
                return 
            
        self.message = "Invalid username or password"

# ================================================= SIGNUP ====================================================

class RegisterUser:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.message = ""
        self.success = False

        if ('.com' not in self.email) or ('@' not in self.email):
            self.message = "Please enter a valid email address"
            return
        
        for user in stored_users_data.values():
            if user.get("email") == self.email:
                self.message = "This email is already registered"
                return    

        for user in stored_users_data.values():
            if user.get("username") == self.username:
                self.message =  "Username already exists"
                return
        
        if len(password) < 6:
            self.message = "Password must be at least 6 characters long"
            return
        
        user_id = str(len(stored_users_data) + 1)

        stored_users_data[user_id] = {
            "username": self.username,
            "email": self.email,
            "password" : hash_password(self.password),
            "plan": "Free"
        }

        save_user_data()

        self.message = "Registration successful"
        self.success = True

# ================================================ LOGOUT ======================================================

class Logout:
    def __init__(self):
        st.session_state.is_logged_in = False
        st.session_state.user = None
        st.session_state.user_id = None
        st.session_state.current_page = "home"
        st.success("Logged out successfully")

# =============================================== PAYMENT SERVICE ===============================================

class Payment:
    def __init__(self, id=None, user_id=None, amount=None, plan=None, status=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.plan = plan
        self.status = status
        self.created_at = created_at or datetime.now()

    @staticmethod
    def create(user_id, amount, plan, status="completed"):
        """Simulate creating a payment record"""
        # In a real app, this would connect to a payment processor and database

        return Payment(
            id=1, # Simulated ID
            user_id=user_id,
            amount=amount,
            plan=plan,
            status=status
        )
    
    @staticmethod
    def get_plan_price(plan):
        """Get the price for a subscription plan"""
        prices = {
            "Free": 0,
            "Basic": 4.99,
            "Pro": 9.99,
            "Enterprise": 19.99
        }

        return prices.get(plan, 0)
    
class PaymentService:
    def process_payment(self, user_id, plan, card_number, expiry, cvv):
        """Simulate Processing A Payment"""
        # In a real app, this would connect to a payment processor

        # simple validation
        if not self._validate_card(card_number, expiry, cvv):
            return False
        
        # Get plan price
        amount = Payment.get_plan_price(plan)

        # Creating payment record
        payment = Payment.create(user_id, amount, plan)

        # Updating user's plan
        stored_users_data[user_id]["plan"] = plan
        save_user_data()

        return payment is not None
    
    def _validate_card(self, card_number, expiry, cvv):
        """Simple validation for card details"""
        # Remove spaces and check if it's a number with correct length
        card_number = card_number.replace(" ", "")
        if not card_number.isdigit() or len(card_number) < 13 or len(card_number) > 19:
            return False
        
        # Checking expiry format (MM/YY)
        if not re.match(r"^\d{2}/\d{2}$", expiry):
            return False
        
        # Checking cvv
        if not cvv.isdigit() or len(cvv) < 3 or len(cvv) > 4:
            return False
        
        return True
    
# ====================================== AI RECEIPT INTERPRETER ================================================

def interpret_receipt(user_input):
    load_dotenv()

    gemini_api_key = os.getenv("GOOGLE_API_KEY")

    if not gemini_api_key:
        return {"error": "Google API Key not found. Please add it to your .env file."}
    
    genai.configure(api_key=gemini_api_key)

    try:
        image = Image.open(user_input)
    except Exception as e:
        return {"error": f"Could not open image: {e}"}
    
    model = genai.GenerativeModel('gemini-1.5-flash') # Use latest Gemini version available

    # Call multimodal model
    response = model.generate_content([
        "Extract the following from this receipt image:\n"
        "1. Merchant name\n"
        "2. List of items (with quantities and prices, if available)\n"
        "3. Total amount\n"
        "4. Expense category (e.g. Meals, Travel)\n"
        "Respond only with raw JSON. Do not include Markdown formatting or explanations.\n"
        "Return everything as a JSON object with keys: merchant, items (list of dicts with name, qty, price), total, category.",
        image
    ])

    try:
        cleaned_text = re.sub(r"^(?:```json|```)$", "", response.text.strip(), flags=re.MULTILINE).strip()
        return json.loads(cleaned_text)
    except Exception as e:
        return {"error": f"Could not parse response. Raw output: {response.text}, Error: {str(e)}"}
    

# ========================================== UTILITY FUNCTIONS ====================================================


def downgrade_plan(user_id):
    stored_users_data[user_id]["plan"] = "Free"
    save_user_data()


def get_user_receipts(user_id):
    """Returns list of receipts for a user"""
    now = datetime.now()
    month_key = f"{now.year}-{now.month:02d}"
    user_receipts = stored_receipts_data.get(user_id, {})
    return user_receipts.get(month_key, [])


def add_user_receipt(user_id, receipt_data):
    """Add a receipt for a user"""
    now= datetime.now()
    month_key = f"{now.year}-{now.month:02d}"

    if user_id not in stored_receipts_data:
        stored_receipts_data[user_id] = {}

    if month_key not in stored_receipts_data[user_id]:
        stored_receipts_data[user_id][month_key] = []

    stored_receipts_data[user_id][month_key].append(receipt_data)
    save_receipt_data()


def can_upload_receipt(user_id):
    """To check if a user can upload more receipts this month"""
    plan = stored_users_data[user_id].get("plan", "Free")

    if plan != "Free":
        return True
    
    return len(get_user_receipts(user_id)) < FREE_RECEIPT_LIMIT


def get_plan(user_id):
    if not user_id or user_id not in stored_users_data:
        return "Free"
    return stored_users_data[user_id].get("plan", "Free")


def format_expense_report(receipt):
    if "error" in receipt:
        return receipt["error"]
    
    merchant = receipt.get("merchant", "N/A")
    items = receipt.get("items", [])
    total = receipt.get("total", "N/A")
    category = receipt.get("category", "N/A")
    report = f"**Merchant:** {merchant}\n\n"
    report += "**Items:**\n"
    if items:
        for item in items:
            name = item.get("name", "Item")
            qty = item.get("qty", 1)
            price = item.get("price", "N/A")
            report += f"- {name} (Qty: {qty}, Price: {price})\n"
    else:
        report += "- No items found\n"
    report += f"\n**Total:** {total}\n"
    report += f"**Category:** {category}\n"
    
    return report


def receipt_to_csv(receipt):
    """Convert a single receipt dict to csv string"""
    
    if "error" in receipt:
        return "Error, No data"
    output = "Merchant,Category,Total,Item Name,Qty,Price\n"
    merchant = receipt.get("merchant", "")
    category = receipt.get("category", "")
    total = receipt.get("total", "")
    items = receipt.get("items", [])

    if not items:
        output += f"{merchant},{category},{total},,,\n"
    else:
        for item in items:
            name = item.get("name", "")
            qty = item.get("qty", "")
            price = item.get("price", "")
            output += f"{merchant},{category},{total},{name},{qty},{price}\n"
    
    return output


def all_receipts_to_csv(receipts):
    """Convert a list of receipts to csv string"""
    output = "Merchant,Category,Total,Item Name,Qty,Price\n"

    for receipt in receipts:
        if "error" in receipt:
            continue
        merchant = receipt.get("merchant", "")
        category = receipt.get("category", "")
        total = receipt.get("total", "")
        items = receipt.get("items", [])
        if not items:
            output += f"{merchant},{category},{total},,,\n"
        else:
            for item in items:
                name = item.get("name", "")
                qty = item.get("qty", "")
                price = item.get("price", "")
                output += f"{merchant},{category},{total},{name},{qty},{price}\n"
    return output


def delete_user_receipt(user_id, month_key, receipt_index):
    """Delete a receipt by index for a user in given month"""

    if user_id in stored_receipts_data and month_key in stored_receipts_data[user_id]:
        try:
            del stored_receipts_data[user_id][month_key][receipt_index]

            # Remove month if empty
            if not stored_receipts_data[user_id][month_key]:
                del stored_receipts_data[user_id][month_key]
            save_receipt_data()
            return True
        
        except Exception:
            return False
    return False


# ========================================== STREAMLIT UI ========================================================

def header():

    col1, col2, col3 = st.columns([5,1,1])

    with col1:
        st.markdown('<div class="receipt-header">🧾AI Receipt Interpreter</div>', unsafe_allow_html=True)
        st.markdown("Automate your expense tracking, save time, and focus on what matters!")
    with col2:
        if st.session_state.get("is_logged_in"):
            user_id = st.session_state.get("user_id")
            user_data = stored_users_data.get(user_id, {})
            username = user_data.get("username", "User")

            # Using initials for avatar
            initials = "".join([x[0].upper() for x in username.split() if x])[:2]
            st.markdown(
                f"""
                <div class="user-info-row">
                    <div class="user-avatar">{initials}</div>
                    <span style="font-weight:600;font-size:1.1rem;color:#334155">{username}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
    with col3:
        if st.session_state.get("is_logged_in"):
            if st.button("Logout"):
                Logout()
                st.session_state.current_page = "login"
                st.rerun()
        else:
            if not st.session_state.get("is_logged_in"):
                if st.button("Login"):
                    st.session_state.current_page = "login"
                    st.rerun()

def sidebar_user_info():
    if st.session_state.get("is_logged_in"):
        with st.sidebar:
            user_id = st.session_state.get("user_id")
            user_data = stored_users_data.get(user_id, {})
            st.subheader(f"Welcome, {user_data.get('username', ' ')}")

            if st.button("Home page"):
                st.session_state.show_receipt_history = False
                st.session_state.show_receipt_details = False
                st.session_state.selected_receipt = None
                st.rerun()

def sidebar_upgrade_plan():
    if st.session_state.get("is_logged_in"):
        with st.sidebar:
            st.subheader("Plan Options")
            user_id = st.session_state.get("user_id")
            current_plan = get_plan(user_id)

            st.markdown(
             f"""
                <i>Current Plan: <b>{current_plan}</b></i>
            """   , unsafe_allow_html= True
            )

            if current_plan == "Free":
                if st.button("Upgrade Plan", key="sidebar_upgrade"):
                    st.session_state.show_upgrade_ui = True
            else:
                if st.button("Downgrade To Free", key="sidebar_downgrade"):
                    downgrade_plan(user_id)
                    st.success("Plan downgraded to Free")
                    st.rerun()


def sidebar_receipt_history():
    if st.session_state.get("is_logged_in"):
        with st.sidebar:
            st.subheader("Receipt History")
            if st.button("View Receipts", key="sidebar_view_receipts"):
                st.session_state.show_receipt_history = True


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
                    st.session_state.is_logged_in = True
                    st.session_state.user = username
                    # Find user_id
                    for user_id, user_data in stored_users_data.items():
                        if user_data.get("username") == username:
                            st.session_state.user_id = user_id
                            break
                    time.sleep(1)
                    st.session_state.show_receipt_history = False
                    st.session_state.show_receipt_details = False
                    st.session_state.selected_receipt = None
                    st.rerun()
                else:
                    st.error(login.message)
        
        st.markdown("Don't have an account?")
        if st.button("Register", key="register_btn"):
            st.session_state.current_page = "register"
            st.rerun()
            
        if st.button("Back to Home", key="back_home_btn"):
            st.session_state.current_page = "home"
            st.session_state.show_receipt_history = False
            st.session_state.show_receipt_details = False
            st.session_state.selected_receipt = None
            st.rerun()


def register_page():
    st.markdown("<h2 style='text-align: center;'>Register</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        with st.form("register_form"):
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Register")
            register = RegisterUser(username, email, password)

            if submit:
                if register.success:
                    st.success(register.message)
                    time.sleep(1)
                    st.session_state.show_receipt_history = False
                    st.session_state.show_receipt_details = False
                    st.session_state.selected_receipt = None
                    st.rerun()
                else:
                    st.error(register.message)
        st.markdown("Already have an account?")
        if st.button("Login", key="login_from_register"):
            st.session_state.current_page = "login"
            st.rerun()

        if st.button("← Back",  key="back_from_create"):
            st.session_state.current_page = "home"
            st.session_state.show_receipt_history = False
            st.session_state.show_receipt_details = False
            st.session_state.selected_receipt = None
            st.rerun()


def upgrade_plan_ui():
    st.subheader("Upgrade Plan")
    st.info("Free plan: 5 receipts/month. Upgrade for unlimited receipts and accounting integration.")
    plans = ["Basic", "Pro", "Enterprise"]
    plan = st.selectbox("Choose a plan",plans)
    st.info(f"**Price: ${Payment.get_plan_price(plan)}** per month")
    card_number = st.text_input("Card Number (0000 0000 0000 0000)", key="card_number")
    expiry = st.text_input("Expiry (MM/YY)", key="expiry")
    cvv = st.text_input("CVV", key="cvv")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Upgrade"):
            service = PaymentService()
            user_id = st.session_state.get("user_id")
            if service.process_payment(user_id, plan, card_number, expiry, cvv):
                st.success("Plan upgraded successfully!")
                st.session_state.show_upgrade_ui = False
                st.rerun()
            else:
                st.error("Payment failed. Please check your card details.")

    with col4: 
        if st.button("Cancel"):
                st.session_state.show_upgrade_ui = False
                st.rerun()


def receipt_history_ui():
    st.subheader("Receipt History (This Month)")
    user_id = st.session_state.get("user_id")
    receipts = get_user_receipts(user_id)
    now = datetime.now()
    month_key = f"{now.year}-{now.month:02d}"

    if st.button("Back to Home"):
        st.session_state.show_receipt_history = False
        st.session_state.show_receipt_details = False
        st.session_state.selected_receipt = None
        st.rerun()
    
    if not receipts:
        st.info("No receipts uploaded this month.")
        return
    
    cols = st.columns(3)
    for i, receipt in enumerate(receipts[::-1]):
        real_index = len(receipts) - 1 - i  # index in stored list

        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="receipt-card">
                    <strong>Merchant:</strong> {receipt.get('merchant', 'N/A')}<br>
                    <strong>Total:</strong> {receipt.get('total', 'N/A')}<br>
                    <strong>Category:</strong> {receipt.get('category', 'N/A')}<br>
                """,
                unsafe_allow_html=True
            )
            if st.button("View Details", key=f"view_{i}"):
                st.session_state.selected_receipt = receipt
                st.session_state.show_receipt_details = True
                st.rerun()

            csv_string = receipt_to_csv(receipt)

            st.download_button(
                "Download CSV",
                csv_string,
                file_name=f"receipt_{i+1}.csv",
                mime="text/csv",
                key=f"csv_{i}"
            )
            st.markdown("</div>", unsafe_allow_html=True)


def receipt_details_ui():

    if st.button("Back to Home"):
        st.session_state.show_receipt_history = False
        st.session_state.show_receipt_details = False
        st.session_state.selected_receipt = None
        st.rerun()

    with st.container():
        st.markdown('<div class="custom-div">', unsafe_allow_html=True)
        
        receipt = st.session_state.get("selected_receipt")

        if receipt:
            with st.container():
                st.subheader("Receipt Details")
                st.markdown(format_expense_report(receipt))

                col1, col2, col3 = st.columns([1,1,2])

                with col1:
                    if st.button("Back to History"):
                        st.session_state.show_receipt_details = False
                        st.session_state.selected_receipt = None
                        st.rerun()
                with col2:
                    if st.button("Delete", key=f"delete"):
                        # Find the index and month_key for the selected receipt
                        user_id = st.session_state.get("user_id")
                        now = datetime.now()
                        month_key = f"{now.year}-{now.month:02d}"
                        receipts = get_user_receipts(user_id)

                        try:
                            real_index = receipts.index(receipt)
                        except ValueError:
                            real_index = None
                        if real_index is not None and delete_user_receipt(user_id, month_key, real_index):
                            st.success("Receipt deleted.")
                            st.session_state.show_receipt_details = False
                            st.session_state.selected_receipt = None
                            st.rerun()
                        else:
                            st.error("Failed to delete receipt.")
                with col3:
                    csv_str = receipt_to_csv(receipt)
                    st.download_button(
                        "Download this Receipt as CSV",
                        csv_str,
                        file_name="receipt.csv",
                        mime="text/csv"
                    )
        st.markdown('<div class="custom-div">', unsafe_allow_html=True)



def main():

    header()
    sidebar_user_info()
    sidebar_upgrade_plan()
    sidebar_receipt_history()

    if not st.session_state.get("is_logged_in"):
        if st.session_state.current_page == "login":
            login_page()
        elif st.session_state.current_page == "register":
            register_page()

    if st.session_state.get("show_upgrade_ui", False):
        upgrade_plan_ui()
        return

    if st.session_state.get("show_receipt_history", False):
        if st.session_state.get("show_receipt_details", False):
            receipt_details_ui()
        else:
            receipt_history_ui()
        return
    
    user_id = st.session_state.get("user_id")

    if not st.session_state.get("is_logged_in") or user_id is None:
        return

    plan = get_plan(user_id)
    st.write(f"**Current Plan:** {plan}")
    if plan == "Free":
        used = len(get_user_receipts(user_id))
        st.info(f"Receipts used this month: {used}/{FREE_RECEIPT_LIMIT}")
        if used >= FREE_RECEIPT_LIMIT:
            st.warning("You have reached your free limit for this month. Please upgrade to continue.")
            if st.button("Upgrade Plan"):
                upgrade_plan_ui()
            return
        
    uploaded_file = st.file_uploader("Upload a receipt image", type=["jpg", "jpeg", "png"])
    if uploaded_file and can_upload_receipt(user_id):
        with st.spinner("Processing..."):
            receipt = interpret_receipt(uploaded_file)
        if "error" in receipt:
            st.error(receipt["error"])
        else:
            add_user_receipt(user_id, receipt)
            st.success("Receipt processed and saved!")
            st.subheader("Extracted Expense Report")
            st.markdown(format_expense_report(receipt))
            csv_string = receipt_to_csv(receipt)
            st.download_button("Export this receipt as CSV", csv_string, file_name="receipt.csv", mime="text/csv")

    st.subheader("Your Receipts This Month")
    receipts = get_user_receipts(user_id)
    if receipts:
        for i, receipt in enumerate(receipts[::-1], 1):
            with st.expander(f"Receipt #{len(receipts)-i+1}"):
                st.markdown(format_expense_report(receipt))
        
        csv_all_receipts = all_receipts_to_csv(receipts)
        st.download_button("Export all receipts as CSV", csv_all_receipts, file_name="all_receipts.csv", mime="text/csv")
    else:
        st.info("No receipts uploaded this month.")

    
    if plan != "Free":
        st.subheader("Accounting Software Integration (Paid Feature)")
        st.info("Integration with accounting software coming soon!")

    if plan == "Free":
        if st.button("Upgrade Plan"):
            upgrade_plan_ui()




if __name__ == "__main__":
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False
    if "show_upgrade_ui" not in st.session_state:
        st.session_state.show_upgrade_ui = False
    if "show_receipt_history" not in st.session_state:
        st.session_state.show_receipt_history = False
    if "show_receipt_details" not in st.session_state:
        st.session_state.show_receipt_details = False
    if "selected_receipt" not in st.session_state:
        st.session_state.selected_receipt = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "login"
    main()