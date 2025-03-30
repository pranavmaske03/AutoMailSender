# Auto Mail Sender 📧

A Python script that logs running processes and automatically emails the log file at scheduled intervals. It ensures efficient process monitoring with minimal effort.

---

## 📌 Features

✅ Logs all running processes with their **PID, name, username, and memory usage**  
✅ **Sends email automatically** with the log file attached  
✅ Uses **environment variables** for secure email credentials  
✅ Implements **internet connectivity check** before sending mail  
✅ Supports **customizable scheduling** for periodic execution  

---

## 🔧 Installation & Setup

### 1️⃣ Clone the repository  
```sh
git clone https://github.com/pranavmaske03/AutoMailSender.git
cd AutoMailSender
```

### 2️⃣ Install dependencies  
```sh
pip install -r requirements.txt
```

### 3️⃣ Create a `.env` file  
Add your email credentials inside a `.env` file in the project directory:  

```sh
SENDER_EMAIL="your-email@gmail.com"
RECEIVER_EMAIL="receiver-email@gmail.com"
EMAIL_APP_PASSWORD="your-app-password"
```

**⚠ Note:** Use an **App Password** instead of your actual email password for security.  

### 4️⃣ Run the script  
```sh
python autosender.py 5  # Runs every 5 minutes
```

---

## 🚀 How It Works  

1️⃣ The script **fetches running processes** and logs them into a file.  
2️⃣ It **checks internet connectivity** before attempting to send an email.  
3️⃣ The **log file is emailed** to the configured receiver.  
4️⃣ The process repeats at **scheduled intervals** using `schedule`.  

---

## 🛠 Improvements & Fixes  

🔹 **Replaced hardcoded credentials** with `.env` file for security.  
🔹 **Fixed incorrect file naming format** for proper timestamped logs.  
🔹 **Added error handling** for invalid email credentials & connection issues.  
🔹 **Ensured graceful script termination** when invalid input is provided.  
🔹 **Added better spacing & readability** in the codebase.  

---

## 📺 Future Enhancements  

💡 Add an option to send logs **only for high-memory processes**  
💡 Implement a **GUI version** for easier configuration  
💡 Allow **multiple recipients** for log reports  
💡 Add **log file compression** before sending  

---

## 🐜 License  

This project is **open-source** and free to use. Contributions are welcome! 🎉  

---

### 🌟 If you find this useful, give it a ⭐ on [GitHub](https://github.com/pranavmaske03/AutoMailSender)!
