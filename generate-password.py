import secrets
import string
import pyperclip
import json

# Common weak passwords list (can be expanded)
WEAK_PASSWORDS = {"password", "123456", "qwerty", "letmein", "12345678", "abcdef"}

def generate_password(length=12, use_upper=True, use_digits=True, use_symbols=True, avoid_ambiguous=True):
    characters = string.ascii_lowercase
    if use_upper:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation
    
    if avoid_ambiguous:
        characters = characters.translate(str.maketrans('', '', '0O1lI|'))
    
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def check_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1
    
    if password in WEAK_PASSWORDS:
        return "Weak (Common Password)"
    
    return ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"][score]

def save_password(password):
    with open("passwords.json", "a") as file:
        json.dump({"password": password}, file)
        file.write("\n")
    print("Password saved to passwords.json")

def main():
    length = int(input("Enter password length: "))
    upper = input("Include uppercase letters? (y/n): ").lower() == 'y'
    digits = input("Include numbers? (y/n): ").lower() == 'y'
    symbols = input("Include symbols? (y/n): ").lower() == 'y'
    ambiguous = input("Avoid ambiguous characters? (y/n): ").lower() == 'y'
    
    password = generate_password(length, upper, digits, symbols, ambiguous)
    strength = check_strength(password)
    
    print(f"Generated Password: {password}")
    print(f"Password Strength: {strength}")
    
    pyperclip.copy(password)
    print("Password copied to clipboard!")
    
    save_option = input("Save password to file? (y/n): ").lower()
    if save_option == 'y':
        save_password(password)

if __name__ == "__main__":
    main()
