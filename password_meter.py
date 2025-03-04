import re
import random
import string
import streamlit as st

COMMON_PASSWORDS = ["password", "123456", "qwerty", "admin", "letmein", "welcome",
                    "password123", "qwerty123", "asdfgh", "zxcvbn", "1111", "12345"]

def has_repeated_chars(password):
    return re.search(r'(.)\1{3,}', password)  # 4+ repeating characters

def is_sequential(s):
    s = s.lower()
    if len(s) < 4:
        return False
    delta = ord(s[1]) - ord(s[0])
    if abs(delta) != 1:
        return False
    for i in range(2, len(s)):
        if ord(s[i]) - ord(s[i-1]) != delta:
            return False
    return True

def has_sequential_pattern(password):
    for i in range(len(password) - 3):
        substring = password[i:i+4]
        if is_sequential(substring):
            return True
    return False

def check_password_strength(password):
    score = 0
    feedback = []
    
    if password.lower() in COMMON_PASSWORDS:
        return 0, ["❌ Password is too common and weak. Please choose a stronger password."]
    
    # Length Check (Weight: 2 score)
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
        feedback.append("ℹ️ Consider using 12+ characters for better security")
    else:
        feedback.append("❌ Password should be at least 8 characters long")
    
    # alag alag characters ko check krega
    checks = {
        'upper_lower': (r'[A-Z].*[a-z]|[a-z].*[A-Z]', "Include both uppercase and lowercase letters"),
        'digit': (r'\d', "Add at least one number (0-9)"),
        'special': (r'[!@#$%^&*]', "Include at least one special character (!@#$%^&*)")
    }
    
    for key, (pattern, message) in checks.items():
        if re.search(pattern, password):
            score += 1
        else:
            feedback.append(f"❌ {message}")
    
    # Advanced Security Checks
    advanced_feedback = []
    if has_repeated_chars(password):
        score -= 1
        advanced_feedback.append("❌ Avoid repeating characters (aaaa, 1111 etc.)")
    
    if has_sequential_pattern(password):
        score -= 1
        advanced_feedback.append("❌ Avoid sequential patterns (abcd, 1234 etc.)")
    
    score = max(0, score)  # negative score ko prevent krega 
    
    # Combine feedback
    if advanced_feedback:
        feedback.append("\nAdvanced Security:")
        feedback.extend(advanced_feedback)
    
    return score, feedback

def generate_strong_password(length=12):
    while True:
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(characters) for _ in range(length))
        if (len(password) >= 8 and
            re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'\d', password) and
            re.search(r'[!@#$%^&*]', password) and
            not has_repeated_chars(password) and
            not has_sequential_pattern(password)):
            return password

def main():
    st.title("🔒 Advanced Password Strength Meter")
    st.write("Check your password security or generate a strong password")

    option = st.radio("Select option:", ("Check Password", "Generate Password"))
    
    if option == "Check Password":
        password = st.text_input("Enter password:", type="password", help="We never store your passwords")
        
        if password:
            score, feedback = check_password_strength(password)
            
            st.subheader("Security Assessment:")
            if score >= 5:
                st.success("✅ Strong Password! (Score: {}/5)".format(score))
            elif score >= 3:
                st.warning("⚠️ Moderate Password (Score: {}/5)".format(score))
            else:
                st.error("❌ Weak Password (Score: {}/5)".format(score))
            
            st.write("### Recommendations:")
            for item in feedback:
                if item.startswith("❌"):
                    st.error(item)
                elif item.startswith("ℹ️"):
                    st.info(item)
                else:
                    st.write(item)
    
    else:
        length = st.number_input("Password length:", min_value=8, max_value=32, value=12)
        if st.button("Generate Secure Password"):
            password = generate_strong_password(length)
            st.success("### Generated Password:")
            st.code(password)
            st.write("Copy this password and store it securely!")

if __name__ == "__main__":
    main()