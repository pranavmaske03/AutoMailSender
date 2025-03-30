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

### Process Monitoring

  The script uses Python's psutil library to monitor all active processes on your computer. When triggered, it scans through each running program and collects four key pieces of information: the process ID (a unique number), the program name, which user account started it, and how much virtual memory it's using. This data gets organized into a Python dictionary for easy handling. The script automatically skips any processes it can't access due to permission issues.

### Log File Creation
Every time the script runs, it generates a new log file with a timestamp in the filename (like "Log_2023-11-15_14-30-00.log"). The file starts with a header showing the exact collection time, followed by a neatly formatted list of all running processes. Each process entry shows the collected information in a consistent layout, making it easy to scan through the report later.

### Email Automation
When configured with Gmail credentials in the .env file, the script can send the log files automatically. It uses Python's built-in smtplib to securely connect to Gmail's email servers. The email includes a friendly message in the body and attaches the latest log file. Before sending, the script checks your internet connection by trying to access youtube.com - if this fails, it waits until the next scheduled run to try again.

### Scheduling System
The heart of the automation is the schedule library. When you start the script (like with python autosender.py 5), it sets up a repeating timer that triggers the monitoring process every X minutes (5 in this example). The timer runs in the background while the script keeps working, using very little computer resources between checks.

### Error Handling
The script includes several safety checks: it verifies your email credentials are properly configured, handles temporary internet outages gracefully, and skips any system processes that can't be accessed normally. If something goes wrong, it shows clear error messages in the console rather than crashing unexpectedly.

---
## 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request.



