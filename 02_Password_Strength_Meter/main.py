import streamlit as st
import re
import random
import string

st.set_page_config(
    page_title="Password Strength Meter",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        margin-top: 1rem;
        background: linear-gradient(to right, #0097ae, #00c2e0);
        font-weight: bold;
        border: 2px solid transparent;
        transition: background 1s ease, border-color 0.5s ease, color 0.5s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(to right, #0097ae, #0097ae);
        border-color: #092d99; 
        color: white;
    }
</style>
""", unsafe_allow_html=True)

common_passwords = [
    "123456", "password", "123456789", "12345", "12345678", "qwerty", "abc123", 
    "password123", "111111", "123123", "admin", "letmein", "welcome", "monkey", 
    "sunshine", "qwertyuiop", "1234", "1q2w3e4r", "password1", "dragon", "iloveyou"
]

def check_password_strength(password):
    score = 0

    # blacklisting common passwords
    if password.lower() in common_passwords:
        st.markdown("❌ Your password is too common. Please choose a stronger one")
        return score  # Return score immediately if the password is common

    if len(password) >= 12:
        score += 1

    # checking length 
    if len(password) >= 8:
        score += 1
    else:
        st.markdown("❌ Password should be at least 8 characters long")

    # uppercase and lowercase check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        st.markdown("❌ Password must include both uppercase and lowercase letters")

    # checking digits
    if re.search(r"\d", password):
        score += 1
    else:
        st.markdown("❌ Add at least one number from (0-9)")

    # checking special characters
    if re.search(r"[!@#$%^&*]", password):
        score += 1 
    else:
        st.markdown("❌ Include at least one special character (!@#$%^&*)")

    return score  # Returning score after checking all conditions

def generate_password(length, use_digits, use_special):
    characters = string.ascii_letters

    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation  # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~

    return ''.join(random.choice(characters) for _ in range(length))

def main():
    # Ensuring that score is stored in session state
    if "score" not in st.session_state:
        st.session_state.score = None

    with st.sidebar:
        st.header("📌 Tips for a Strong Password:")
        st.info(""" 
        - **Length matters:** Use a password that is at least 12 characters long for better security.
        - **Mix it up:** Include uppercase and lowercase letters, numbers, and special characters (e.g., !, @, #, $).
        - **Avoid common patterns:** Don't use easily guessable information, such as your name, birthdate, or simple sequences (e.g., 1234, qwerty).
        - **Use a passphrase:** Consider a random combination of unrelated words or a memorable sentence to increase strength.
        - **Enable 2FA:** For an added layer of security, always enable two-factor authentication (2FA) where possible.
        - **Don’t reuse passwords:** Avoid using the same password across multiple accounts. Use a password manager to help you keep track of them.
        """)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.title("Password Strength Meter 🧭")
        st.write("Stronger passwords, safer you. Build it strong, keep it secure!")

        st.markdown("Check the strength of your password")
        input_password = st.text_input("Enter your password here", type="password", help="Password should be at least 8-12 characters long and include a mix of uppercase, lowercase, numbers, and special characters.")

        if st.button("Check Strength") and input_password:
            st.session_state.score = check_password_strength(input_password)

    if st.session_state.score is not None:
        with col2:
            st.markdown(f"Password Strength Score: **{st.session_state.score}**")
            st.progress(st.session_state.score / 5)

            if st.session_state.score == 5:
                st.info("✅ **Excellent Password!** You've created a top-tier password that meets all the criteria for maximum security! Keep it safe and secure 👏")
            elif st.session_state.score == 4:
                st.info("✅ Strong Password!")
            elif st.session_state.score == 3:
                st.info("⚠️ Moderate Password - Consider adding more security features given in the sidebar..")
            else:
                st.info("❌ Weak Password - Improve it using the suggestions given in the sidebar.")
            
            if st.session_state.score <= 4:
                with st.expander("Generate Strong Password"):
                    length = st.slider("Select password length", min_value=8, max_value=20, value=12)

                    use_digits = st.checkbox("Include digits")
                    use_special = st.checkbox("Include special characters")

                    if st.button("Generate Password"):
                        password = generate_password(length, use_digits, use_special)
                        st.write("Generated Password:")
                        st.code(password)

if __name__ == "__main__":
    main()