import hashlib
import requests
import time
import random
import string
import math
from colorama import Fore, Style, init
import os

# Initialize colorama for colored terminal output
init(autoreset=True)

# Function to calculate password entropy
def calculate_entropy(password):
    character_set = 0
    if any(c.islower() for c in password): character_set += 26
    if any(c.isupper() for c in password): character_set += 26
    if any(c.isdigit() for c in password): character_set += 10
    if any(c in string.punctuation for c in password): character_set += len(string.punctuation)
    
    if character_set == 0:
        return 0  # Empty or invalid password
    return len(password) * math.log2(character_set)

# Function to estimate password cracking time
def estimate_crack_time(entropy):
    guesses_per_second = 1e12  # Assumes a powerful attacker with a trillion guesses per second
    seconds = 2**entropy / guesses_per_second
    if seconds < 60:
        return "🔴 Instantly cracked! Use a much stronger password."
    elif seconds < 3600:
        return "🟠 Can be cracked within an hour. Consider strengthening it."
    elif seconds < 86400:
        return "🟡 Can be cracked within a day. Increase complexity."
    elif seconds < 31536000:
        return "🟢 Can last a year against brute-force attacks. Still, be cautious."
    else:
        return "🟢🔒 Practically uncrackable in a human lifetime! Great job."

# Function to explain entropy
def explain_entropy(entropy):
    if entropy < 28:
        return "🔴 Very weak: Easily cracked in seconds by brute force. Consider using a much stronger password."
    elif entropy < 35:
        return "🟠 Fair: Could be cracked within hours. Improve by adding more unique characters."
    elif entropy < 50:
        return "🟡 Good: Strong enough for most accounts, but could be improved further."
    else:
        return "🟢 Very strong: Extremely difficult to crack. Great job!"

# Function to check if a password has been leaked using Have I Been Pwned
def check_hibp(password):
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]

    print(Fore.CYAN + "➡️  Checking Have I Been Pwned... ⏳")
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    if response.status_code != 200:
        print(Fore.RED + "⚠️ Error checking HIBP! Skipping this step.")
        return False, 0

    hashes = response.text.splitlines()
    for line in hashes:
        h, count = line.split(":")
        if h == suffix:
            print(Fore.RED + f"❌ Found in Have I Been Pwned ({count} breaches)!")
            return True, int(count)  # Password is leaked

    print(Fore.GREEN + "✅ Not found in Have I Been Pwned!")
    return False, 0  # Password not found

# Function to suggest a better password
def suggest_better_password(password):
    modifications = [
        lambda p: p + random.choice(string.punctuation),  # Add a special character
        lambda p: p + str(random.randint(10, 99)),  # Add a random number
        lambda p: ''.join(random.choice(string.ascii_letters) for _ in range(3)) + p,  # Add random letters at start
        lambda p: p.replace("a", "@").replace("i", "1").replace("o", "0").replace("e", "3")  # Replace common letters
    ]

    # Apply 2 random modifications
    modified_password = password
    for _ in range(2):
        modified_password = random.choice(modifications)(modified_password)

    return modified_password

# Function to save results to a file
def save_results(password, strength, entropy, is_leaked, breach_count, suggested_password):
    filename = "password_results.txt"
    with open(filename, "a") as f:
        f.write(f"Password: {password}\n")
        f.write(f"Strength: {strength}\n")
        f.write(f"Entropy: {entropy:.2f} bits\n")
        f.write(f"Entropy Explanation: {explain_entropy(entropy)}\n")
        f.write(f"Estimated Crack Time: {estimate_crack_time(entropy)}\n")
        f.write(f"Leaked: {'Yes' if is_leaked else 'No'}\n")
        if is_leaked:
            f.write(f"Breaches: {breach_count}\n")
        f.write(f"Suggested Fix: {suggested_password}\n")
        f.write("="*40 + "\n")
    
    print(Fore.GREEN + f"✅ Results saved to {filename}.")

# Main script
if __name__ == "__main__":
    while True:
        print(Fore.BLUE + Style.BRIGHT + "🔒 Enhanced Password Strength Checker 🔒")
        user_password = input("Enter a password to check: ")

        # Check strength and entropy
        strength, entropy = "Weak", calculate_entropy(user_password)

        if entropy < 28:
            strength = Fore.RED + "Weak"
        elif entropy < 35:
            strength = Fore.YELLOW + "Fair"
        else:
            strength = Fore.GREEN + "Strong"

        print(f"\n🔹 Password Strength: {strength}")
        print(f"🔹 Entropy Score: {entropy:.2f} bits")
        print(f"📢 {explain_entropy(entropy)}")
        print(f"🕒 Estimated Crack Time: {estimate_crack_time(entropy)}")

        # Check password leaks
        is_leaked, breach_count = check_hibp(user_password)

        better_password = suggest_better_password(user_password)
        print(Fore.GREEN + f"✅ Suggested Stronger Password: {better_password}")

        if is_leaked:
            print(Fore.RED + f"❌ Your password has been leaked {breach_count} times! DO NOT USE IT.")
        else:
            print(Fore.GREEN + "✅ Your password has NOT been found in known leaks.")
        
        another_password = input(Fore.YELLOW + "\nWould you like to check another password? (yes/no): ").strip().lower()
        if another_password not in ["yes", "y"]:
            break

    # Ask to save results
    save_choice = input(Fore.YELLOW + "\nWould you like to save the results to a file? (yes/no): ").strip().lower()
    if save_choice in ["yes", "y"]:
        save_results(user_password, strength, entropy, is_leaked, breach_count, better_password)
