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
    """Checks internet connectivity by pinging YouTube."""
    try:
        urllib2.urlopen('http://www.youtube.com', timeout=1)
        return True
    except urllib2.URLError:
        return False

def GetProcessInfo():
    """
    Retrieves running processes with:
    - PID, name, username
    - Memory usage (VMS in MB and percentage)
    """
    listprocess = []
    
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'memory_percent'])
            pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)  # Virtual Memory Size in MB
            listprocess.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    # Sort by memory usage (descending)
    return sorted(listprocess, key=lambda x: x['memory_percent'], reverse=True)

def MailSender(filename, log_time):    
    """Sends email with formatted log file attachment."""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"Process log generated at: {log_time}"

        body = f"""
        Hello {RECEIVER_EMAIL},
        
        Please find attached the system process log.
        
        Report generated at: {log_time}
        
        This is an auto-generated email.
        
        Regards,
        Process Monitor
        """
        msg.attach(MIMEText(body, 'plain'))

        with open(filename, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(filename)}"')
        msg.attach(part)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, EMAIL_APP_PASSWORD)
            server.send_message(msg)
        
        print(f"Email sent successfully in {time.time() - start_time:.2f} seconds")
    
    except smtplib.SMTPAuthenticationError:
        print("Error: Email authentication failed. Check your .env credentials.")
    except smtplib.SMTPException as e:
        print(f"SMTP Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

def ProcessLog(log_dir='LogFile'):
    """Generates formatted process log and triggers email."""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
    log_path = os.path.join(log_dir, f"ProcessLog_{timestamp}.log")
    
    processes = GetProcessInfo()
    
    with open(log_path, 'w') as f:
        # Formatted header
        f.write("="*80 + "\n")
        f.write(f"SYSTEM PROCESS REPORT - {time.ctime()}\n")
        f.write("="*80 + "\n\n")
        
        # Column headers
        f.write(f"{'PID':<8}{'Name':<25}{'User':<20}{'Memory %':<12}{'VMS (MB)':<12}\n")
        f.write("-"*80 + "\n")
        
        # Process entries
        for proc in processes:
            f.write(f"{proc['pid']:<8}{proc['name'][:24]:<25}{proc['username'][:19]:<20}"
                    f"{proc['memory_percent']:<12.2f}{proc['vms']:<12.2f}\n")
    
    print(f"Log generated: {log_path}")
    
    if is_connected():
        start_time = time.time()
        MailSender(log_path, time.ctime())
    else:
        print("Skipped email - No internet connection")

def main():
    """Main execution with scheduling."""
    print(f"{' Auto Process Monitor ':=^40}")
    print(f"Started: {time.ctime()}")
    
    if len(argv) != 2:
        print("Error : please enter the time interval...")
        print("Usage: python autosender.py <interval_minutes>")
        exit(1)
        
    try:
        interval = int(argv[1])
        if interval <= 0:
            raise ValueError("Interval must be > 0")
            
        # Immediate first run
        ProcessLog() 
        
        # Scheduled runs
        schedule.every(interval).minutes.do(ProcessLog)
        
        while True:
            schedule.run_pending()
            time.sleep(1)
            
    except ValueError as e:
        print(f"Error: {str(e)}")
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
