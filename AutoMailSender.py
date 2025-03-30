import os
import time
import psutil
import smtplib
import urllib.request as urllib2
import schedule
from sys import argv
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

if not SENDER_EMAIL or not RECEIVER_EMAIL or not EMAIL_APP_PASSWORD:
    print("Error: Missing environment variables. Please check your .env file.")
    exit(1)

def is_connected():
    """Checks internet connectivity."""
    try:
        urllib2.urlopen('http://www.youtube.com', timeout=1)
        return True
    except urllib2.URLError:
        return False

def GetProcessInfo():
    """Retrieves a list of running processes with details."""
    listprocess = []
    
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            vms = proc.memory_info().vms / (1024 * 1024)
            pinfo['vms'] = vms
            listprocess.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return listprocess

def MailSender(filename, log_time):    
    """Sends an email with the log file as an attachment."""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"Process log file generated at: {log_time}"

        body = f"""
        Hello {RECEIVER_EMAIL},
        
        Welcome to Marvellous Infosystems.
        
        Please find attached document which contains Log of Running process.
        
        Log file is created at: {log_time}
        
        This is an auto-generated mail.
        
        Thanks & Regards,
        Auto Mailer
        """
        msg.attach(MIMEText(body, 'plain'))

        with open(filename, "rb") as attachment:
            p = MIMEBase('application', 'octet-stream')
            p.set_payload(attachment.read())
        
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(p)

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(SENDER_EMAIL, EMAIL_APP_PASSWORD)
        s.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        s.quit()
        
        print("Log file successfully sent through Mail")
    
    except smtplib.SMTPAuthenticationError:
        print("Error: Authentication failed. Check your email and password in the .env file.")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as E:
        print(f"Unexpected error: {E}")

def ProcessLog(log_dir='LogFile'):
    """Generates a log file of running processes and sends it via email."""
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    
    log_path = os.path.join(log_dir, f"Log_{time.strftime('%Y-%m-%d_%H-%M-%S')}.log")
    
    with open(log_path, 'w') as f:
        f.write("-" * 80 + "\n")
        f.write("Process Logger: " + time.ctime() + "\n")
        f.write("-" * 80 + "\n\n")
        for element in GetProcessInfo():
            f.write(f"{element}\n")
    
    print(f"Log file is successfully generated at location {log_path}")
    
    if is_connected():
        start_time = time.time()
        MailSender(log_path, time.ctime())
        print(f'Took {time.time() - start_time:.2f} seconds to send mail')
    else:
        print("There is no Internet connection")

def main():
    """Main function to schedule and run the process logger."""
    print("----Auto Mail Sender-----")
    print("Application name: " + argv[0])
    
    if len(argv) != 2:
        print("Error: Invalid number of arguments")
        exit()
    
    if argv[1] in ["-h", "--H"]:
        print("This script is used to log records of running processes")
        exit()
    
    if argv[1] in ["-u", "--U"]:
        print("Usage: Application AbsolutePath_of_Directory")
        exit()
    
    try:
        interval = int(argv[1])
        if interval <= 0:
            raise ValueError("Interval must be a positive number.")

        schedule.every(interval).minutes.do(ProcessLog)
        
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    except ValueError:
        print("Error: Invalid datatype of input")
    except Exception as E:
        print("Error: Invalid input:", E)

if __name__ == "__main__":
    main()
