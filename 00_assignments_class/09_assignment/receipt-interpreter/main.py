# from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
# from dotenv import load_dotenv
# from datetime import datetime
# import streamlit as st
# from PIL import Image
# import asyncio
# import hashlib
# import base64
# import json
# import csv
# import os
# import re

# st.set_page_config(
#     page_title="AI Receipt Interpreter",
#     page_icon="📜",
#     layout="wide"
# )

# USERS_STORAGE_FILE = "users.json"
# LOCKOUT_DURATION = 500


# # ========================================= Loading user data =====================================================================
# stored_user_data = {}

# if os.path.exists(USERS_STORAGE_FILE):
#     with open(USERS_STORAGE_FILE, "r") as file:
#         stored_data = json.load(file)

# def save_user_data():
#     with open(USERS_STORAGE_FILE, "w") as file:
#         json.dump(stored_data, file)

# # ======================================== Password encryption =========================================================
# def hash_password(password):
#     salt = os.urandom(16) # Random secure salt
#     hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
#     return base64.b64encode(salt + hashed).decode()

# def verify_password(password, stored_value):
#     decoded = base64.b64decode(stored_value.encode())
#     salt = decoded[:16]
#     stored_hash = decoded[16:] 
#     new_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt ,100_000)
#     return new_hash == stored_hash  


# failed_attempts = 0

# def is_locked_out():
#     return st.session_state.get("failed_attempts", 0) >= 3


# # =============================================== CLASSES ===================================================
# # =============================================== Login ======================================================

# class Login:
#     def __init__(self, username, password, email= None):
#         self.username = username
#         self.email = email | None
#         self.password = password
#         self.message = ""
#         self.success = False

#         for user_id, user_data in stored_user_data.items():
#             if user_data.get("username") == username or user_data.get("email") == email and verify_password(password, user_data.get("password")):
#                 st.session_state.is_logged_in = True
#                 st.session_state.user = username
#                 st.session_state.user_id = user_id
#                 self.message = "Login succesful"
#                 self.success = True
#                 return 
        
#         self.message = "Invalid username or password"

# # ============================================= Signup =========================================================

# class RegisterUser:
#     def __init__(self, username, email, password):
#         self.username = username
#         self.email = email
#         self.password = password
#         self.message = ""
#         self.success = False

#         if '.com' and '@' not in self.email:
#             self.message = "Please enter a valid email address"
#             return

#         for email in stored_user_data.values():
#             if email.get("email") == self.email:
#                 self.message = "This email is already registered"
#                 return    

#         for user in stored_user_data.values():
#             if user.get("username") == self.username:
#                 self.message =  "Username already exists"
#                 return

#         if len(password) < 6:
#             self.message = "Password must be at least 6 characters long"
#             return
        
#         user_id = str(len(stored_user_data) + 1)
#         stored_user_data[user_id] = {
#             "username" : self.username,
#             "password" : hash_password(self.password)
#         }

#         save_user_data()
#         self.message = "Registration successful"
#         self.success = True

# # ============================================== Logout ===========================================================
# class Logout:
#     def __init__(self):
#         st.session_state.is_logged_in = False
#         st.session_state.user = None
#         st.session_state.user_id = None
#         st.message = "Logged out succesfully"
#         st.session_state.current_page = "home"

# # =========================================== Payment Service ======================================================


# class Payment:
#     def __init__(self, id=None, user_id=None, amount=None, plan=None, status=None, created_at=None):
#         self.id = id
#         self.user_id = user_id
#         self.amount = amount
#         self.plan = plan
#         self.status = status
#         self.created_at = created_at or datetime.now()
    
#     @staticmethod
#     def create(user_id, amount, plan, status="completed"):
#         """Simulate creating a payment record"""
#         # In a real app, this would connect to a payment processor and database
#         return Payment(
#             id=1,  # Simulated ID
#             user_id=user_id,
#             amount=amount,
#             plan=plan,
#             status=status
#         )
    
#     @staticmethod
#     def get_plan_price(plan):
#         """Get the price for a subscription plan"""
#         prices = {
#             "Free": 0,
#             "Basic": 9.99,
#             "Pro": 19.99,
#             "Enterprise": 49.99
#         }
#         return prices.get(plan, 0)

# class PaymentService:
#     def process_payment(self, user_id, plan, card_number, expiry, cvv):
#         """Simulate processing a payment"""
#         # In a real app, this would connect to a payment processor
        
#         # Simple validation
#         if not self._validate_card(card_number, expiry, cvv):
#             return False
        
#         # Get plan price
#         amount = Payment.get_plan_price(plan)
        
#         # Create payment record
#         payment = Payment.create(user_id, amount, plan)
        
#         return payment is not None
    
#     def _validate_card(self, card_number, expiry, cvv):
#         """Simple validation for card details"""
#         # Remove spaces and check if it's a number with correct length
#         card_number = card_number.replace(" ", "")
#         if not card_number.isdigit() or len(card_number) < 13 or len(card_number) > 19:
#             return False
        
#         # Check expiry format (MM/YY)
#         if not re.match(r"^\d{2}/\d{2}$", expiry):
#             return False
        
#         # Check CVV
#         if not cvv.isdigit() or len(cvv) < 3 or len(cvv) > 4:
#             return False
        
#         return True


# # ============================================ AI Receipt Intrepreter =============================================
# def interpret_receipt(user_input):
    
#     load_dotenv()

#     gemini_api_key = os.getenv("GOOGLE_API_KEY")

#     if not gemini_api_key:
#         return "Error: Google API Key not found. Please add it to your .env file."
    
#     provider = AsyncOpenAI(
#         api_key= gemini_api_key,
#         base_url="https://generativelanguage.googleapis.com/v1beta/openai"
#     )

#     model = OpenAIChatCompletionsModel(
#         model= "gemini-2.0-flash",
#         openai_client= provider
#     )

#     agent = Agent(
#         name = "AI Receipt Interpreter",
#         instructions= """
#             When the user uploads a photo of a receipt, extract the following information:

#             1. Merchant name
#             2. List of purchased items (with quantities and prices, if available)
#             3. Total amount

#             Then:
#             4. Identify and tag the expense category (e.g., Meals, Travel, Office Supplies)
#             5. Generate a structured expense report containing all extracted and categorized information.
#             """ ,
#         model= model
#     )

#     image = Image.open(user_input)

#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     result = loop.run_until_complete(Runner.run(agent, image))
#     loop.close()

#     return result.final_output


# def header():

#     col1, col2, col3 = st.columns([5,1,1])

#     with col1:
#         st.header("AI Receipt Interpreter")

# def main():
     
#     header()


# if __name__ == "__main__":
#     main()


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
import re
from datetime import datetime
import io
import tempfile

st.set_page_config(
    page_title="AI Receipt Interpreter",
    page_icon="📜",
    layout="wide"
)

USERS_STORAGE_FILE = "users.json"
RECEIPTS_STORAGE_FILE = "receipts.json"
LOCKOUT_DURATION = 500
FREE_RECEIPT_LIMIT = 5

# ========================================= Loading user data =====================================================================
stored_user_data = {}
stored_receipt_data = {}

if os.path.exists(USERS_STORAGE_FILE):
    with open(USERS_STORAGE_FILE, "r") as file:
        stored_user_data = json.load(file)

if os.path.exists(RECEIPTS_STORAGE_FILE):
    with open(RECEIPTS_STORAGE_FILE, "r") as file:
        stored_receipt_data = json.load(file)

def save_user_data():
    with open(USERS_STORAGE_FILE, "w") as file:
        json.dump(stored_user_data, file)

def save_receipt_data():
    with open(RECEIPTS_STORAGE_FILE, "w") as file:
        json.dump(stored_receipt_data, file)

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
    def __init__(self, username, password, email=None):
        self.username = username
        self.email = email or None
        self.password = password
        self.message = ""
        self.success = False

        for user_id, user_data in stored_user_data.items():
            if (user_data.get("username") == username or user_data.get("email") == email) and verify_password(password, user_data.get("password")):
                st.session_state.is_logged_in = True
                st.session_state.user = username
                st.session_state.user_id = user_id
                self.message = "Login successful"
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

        if ('.com' not in self.email) or ('@' not in self.email):
            self.message = "Please enter a valid email address"
            return

        for user in stored_user_data.values():
            if user.get("email") == self.email:
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
            "email": self.email,
            "password" : hash_password(self.password),
            "plan": "Free"
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
        st.session_state.current_page = "home"
        st.success("Logged out successfully")

# =========================================== Payment Service ======================================================

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
            id=1,  # Simulated ID
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
            "Basic": 9.99,
            "Pro": 19.99,
            "Enterprise": 49.99
        }
        return prices.get(plan, 0)

class PaymentService:
    def process_payment(self, user_id, plan, card_number, expiry, cvv):
        """Simulate processing a payment"""
        # In a real app, this would connect to a payment processor
        
        # Simple validation
        if not self._validate_card(card_number, expiry, cvv):
            return False
        
        # Get plan price
        amount = Payment.get_plan_price(plan)
        
        # Create payment record
        payment = Payment.create(user_id, amount, plan)
        
        # Update user plan
        stored_user_data[user_id]["plan"] = plan
        save_user_data()
        
        return payment is not None
    
    def _validate_card(self, card_number, expiry, cvv):
        """Simple validation for card details"""
        # Remove spaces and check if it's a number with correct length
        card_number = card_number.replace(" ", "")
        if not card_number.isdigit() or len(card_number) < 13 or len(card_number) > 19:
            return False
        
        # Check expiry format (MM/YY)
        if not re.match(r"^\d{2}/\d{2}$", expiry):
            return False
        
        # Check CVV
        if not cvv.isdigit() or len(cvv) < 3 or len(cvv) > 4:
            return False
        
        return True

# ============================================ AI Receipt Interpreter =============================================
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
            Output the result as a JSON object with keys: merchant, items (list of dicts with name, qty, price), total, category.
            """ ,
        model= model
    )

    # Save uploaded file to a temp file and pass the path
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(user_input.read())
        tmp_path = tmp.name

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(Runner.run(agent, tmp_path))
    loop.close()

    # Try to parse as JSON
    try:
        output = result.final_output.strip()
        # Remove code block markers if present
        if output.startswith("```json"):
            output = output[len("```json"):].strip()
        if output.startswith("```"):
            output = output[3:].strip()
        if output.endswith("```"):
            output = output[:-3].strip()
        return json.loads(output)
    except Exception:
        return {"error": "Could not parse receipt. Raw output: " + str(result.final_output)}
# ============================================ Utility Functions =============================================

def get_user_receipts(user_id):
    """Return list of receipts for a user (this month)"""
    now = datetime.now()
    month_key = f"{now.year}-{now.month:02d}"
    user_receipts = stored_receipt_data.get(user_id, {})
    return user_receipts.get(month_key, [])

def add_user_receipt(user_id, receipt_data):
    """Add a receipt for a user (this month)"""
    now = datetime.now()
    month_key = f"{now.year}-{now.month:02d}"
    if user_id not in stored_receipt_data:
        stored_receipt_data[user_id] = {}
    if month_key not in stored_receipt_data[user_id]:
        stored_receipt_data[user_id][month_key] = []
    stored_receipt_data[user_id][month_key].append(receipt_data)
    save_receipt_data()

def can_upload_receipt(user_id):
    """Check if user can upload more receipts this month"""
    plan = stored_user_data[user_id].get("plan", "Free")
    if plan != "Free":
        return True
    return len(get_user_receipts(user_id)) < FREE_RECEIPT_LIMIT

def get_plan(user_id):
    return stored_user_data[user_id].get("plan", "Free")

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
    """Convert a single receipt dict to CSV string"""
    if "error" in receipt:
        return "Error,No data"
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
    """Convert a list of receipts to CSV string"""
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

# ============================================ Streamlit UI =============================================

def header():
    col1, col2, col3 = st.columns([5,1,1])
    with col1:
        st.header("AI Receipt Interpreter")
    with col2:
        if st.session_state.get("is_logged_in"):
            st.write(f"👤 {st.session_state.get('user')}")
    with col3:
        if st.session_state.get("is_logged_in"):
            if st.button("Logout"):
                Logout()

def login_signup_ui():
    st.subheader("Login or Register")
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            login = Login(username, password)
            if login.success:
                st.success(login.message)
                st.session_state.is_logged_in = True
                st.session_state.user = username
                # Find user_id
                for user_id, user_data in stored_user_data.items():
                    if user_data.get("username") == username:
                        st.session_state.user_id = user_id
                        break
                st.rerun()
            else:
                st.error(login.message)
    with tab2:
        username = st.text_input("New Username")
        email = st.text_input("Email")
        password = st.text_input("New Password", type="password")
        if st.button("Register"):
            reg = RegisterUser(username, email, password)
            if reg.success:
                st.success(reg.message)
            else:
                st.error(reg.message)

def upgrade_plan_ui():
    st.subheader("Upgrade Plan")
    st.info("Free plan: 5 receipts/month. Upgrade for unlimited receipts and accounting integration.")
    plans = ["Basic", "Pro", "Enterprise"]
    plan = st.selectbox("Choose a plan", plans)
    st.write(f"Price: ${Payment.get_plan_price(plan)} per month")
    card_number = st.text_input("Card Number")
    expiry = st.text_input("Expiry (MM/YY)")
    cvv = st.text_input("CVV")
    if st.button("Upgrade"):
        service = PaymentService()
        user_id = st.session_state.get("user_id")
        if service.process_payment(user_id, plan, card_number, expiry, cvv):
            st.success("Plan upgraded successfully!")
        else:
            st.error("Payment failed. Please check your card details.")

def main():
    header()
    if not st.session_state.get("is_logged_in"):
        login_signup_ui()
        return

    user_id = st.session_state.get("user_id")
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
            csv_str = receipt_to_csv(receipt)
            st.download_button("Export this receipt as CSV", csv_str, file_name="receipt.csv", mime="text/csv")

    st.subheader("Your Receipts This Month")
    receipts = get_user_receipts(user_id)
    if receipts:
        for i, receipt in enumerate(receipts[::-1], 1):
            with st.expander(f"Receipt #{len(receipts)-i+1}"):
                st.markdown(format_expense_report(receipt))
        csv_all = all_receipts_to_csv(receipts)
        st.download_button("Export all receipts as CSV", csv_all, file_name="all_receipts.csv", mime="text/csv")
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
    main()