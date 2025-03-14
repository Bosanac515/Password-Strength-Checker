Password Audit

📌 Overview

Password Audit is a Python-based tool that analyzes password strength, checks if it has been leaked in data breaches, estimates cracking time, and provides suggestions for stronger passwords.

🚀 Features

Password Strength Evaluation: Analyzes entropy and categorizes strength as Weak, Fair, or Strong.

Breach Detection: Checks if the password has been compromised using the Have I Been Pwned API.

Entropy & Cracking Time Estimation: Estimates how long it would take to crack the password.

Password Improvement Suggestions: Recommends modifications to strengthen weak passwords.

File Logging: Option to save password analysis results.

📥 Installation

1️⃣ Install Python

Ensure you have Python 3 installed. Check with:

python --version

If not installed, download it from python.org.

2️⃣ Install Required Dependencies

Install the necessary Python libraries:

pip install requests colorama

▶️ Running the Script

Open a terminal (CMD, PowerShell, or Terminal on Mac/Linux).

Navigate to the script's directory:

cd path/to/password_audit

Run the script:

python password_audit.py

📊 Understanding Results

Entropy Score: Measures password unpredictability.

Below 28 bits: Very Weak 🔴

28 - 35 bits: Fair 🟠

35 - 50 bits: Good 🟡

Above 50 bits: Strong 🟢

Cracking Time Estimates:

🔴 Instantly cracked → Too weak!

🟠 Hours to crack → Improve!

🟡 Days to crack → Better, but can be stronger.

🟢 Years/Lifetime to crack → Strong & secure.

Breach Detection:

✅ "Your password has NOT been found in known leaks."

❌ "Your password has been leaked X times! DO NOT USE IT."

Suggested Stronger Password:

If weak, the program will generate a stronger alternative.

🔄 Checking Multiple Passwords

The program will ask if you want to check another password before exiting.

💾 Saving Results

At the end of the scan, you can choose to save results to password_results.txt for future reference.

🛠 Future Improvements

Support for additional breach databases.

GUI version for better usability.

Advanced password generation features.

📝 License

This project is open-source and free to use. Contributions are welcome!

