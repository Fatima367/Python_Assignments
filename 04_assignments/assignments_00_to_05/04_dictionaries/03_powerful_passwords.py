from hashlib import sha256

def login(email, stored_logins, password_to_check):
    """
    Returns True if the hash of the password we are checking matches the one in stored_logins
    for a specific email. Otherwise, returns False.

    email: the email we are checking the password for
    stored_logins: a dictionary pointing from an email to its hashed password
    password_to_check: a password we want to test alongside the email to login with
    """

    if stored_logins[email] == hash_password(password_to_check):
        return True
    
    return False

def hash_password(password):
    """
    Takes in a password and returns the SHA256 hashed value for that specific password.
    
    Inputs:
        password: the password we want
    
    Outputs:
        the hashed form of the input password
    """

    return sha256(password.encode()).hexdigest()

def main():
    # dictionary with emails as keys and hashed passwords as value

    stored_logins = {
        "example@gmail.com": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
        "code_in_placer@cip.org": "973607a4ae7b4cf7d96a100b0fb07e8519cc4f70441d41214a9f811577bb06cc",
        "student@stanford.edu": "882c6df720fd99f5eebb1581a1cf975625cea8a160283011c0b9512bb56c95fb"
    }

    # Created variables instead of duplicating the email literals "student@stanford.edu", 
    # "code_in_placer@cip.org" and "student@stanford.edu" 3 times.

    first_email = "example@gmail.com"
    second_email = "code_in_placer@cip.org"
    third_email = "student@stanford.edu"
    
    print(login(first_email, stored_logins, "word"))
    print(login(first_email, stored_logins, "password"))
    
    print(login(second_email, stored_logins, "Karel"))
    print(login(second_email, stored_logins, "karel"))
    
    print(login(third_email, stored_logins, "password"))
    print(login(third_email, stored_logins, "123!456?789"))


if __name__ == '__main__':
    main()