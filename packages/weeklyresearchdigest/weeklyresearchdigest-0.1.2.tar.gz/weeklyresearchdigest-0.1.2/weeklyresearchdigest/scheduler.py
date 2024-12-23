import os
import platform
import subprocess
from pathlib import Path
from weeklyresearchdigest.weekly_digest import check_and_populate_config
from dotenv import set_key

# Conditionally import crontab for Linux/macOS
if platform.system() in ["Linux", "Darwin"]:
    from crontab import CronTab

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.env")

def schedule_digest():
    """
    Schedule the weekly digest with specific queries on specific days and times.
    """
    print("Welcome to the Weekly Digest Scheduler!")
    
    # Get user inputs
    query = input("Enter the query for this schedule (e.g., 'neuroscience'): ").strip()
    day = input("Enter the day of the week for the digest (e.g., 'Monday'): ").strip().capitalize()
    time = input("Enter the time to send the digest in HH:MM (24-hour format): ").strip()

    if day not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        print("Invalid day entered. Please try again.")
        return

    # Validate time format
    if not validate_time(time):
        print("Invalid time format. Please enter a valid 24-hour time in HH:MM format.")
        return

    # Update the default query in config.env
    if query:
        set_key(CONFIG_FILE, "DEFAULT_QUERY", query)
        print(f"Updated DEFAULT_QUERY in config.env to: {query}")

    # Check the current operating system
    system = platform.system()

    if system == "Windows":
        schedule_windows(day, time, query)
    elif system == "Linux" or system == "Darwin":  # Darwin is macOS
        schedule_unix(day, time, query)
    else:
        print(f"Unsupported operating system: {system}")
        return
    
    print(f"Scheduled digest for '{query}' on {day} at {time} successfully!")

def validate_time(time_str):
    """
    Validate the time string format HH:MM (24-hour format).
    """
    try:
        hours, minutes = map(int, time_str.split(":"))
        return 0 <= hours < 24 and 0 <= minutes < 60
    except ValueError:
        return False

def schedule_windows(day, time, query):
    """
    Schedule the digest on Windows using Task Scheduler and ensure paths are correct.
    """
    task_name = f"WeeklyDigest-{query}-{day}"
    script_path = str(Path(__file__).resolve().parent / "weekly_digest.py")
    venv_path = str(Path(__file__).resolve().parent.parent / "venv" / "Scripts" / "python.exe")

    # Check if paths exist
    if not os.path.exists(script_path):
        print(f"Error: Script file not found at {script_path}")
        return
    if not os.path.exists(venv_path):
        print(f"Error: Python executable not found at {venv_path}")
        return

    # Map day to Windows Task Scheduler format
    day_map = {
        "Monday": "MON",
        "Tuesday": "TUE",
        "Wednesday": "WED",
        "Thursday": "THU",
        "Friday": "FRI",
        "Saturday": "SAT",
        "Sunday": "SUN"
    }
    windows_day = day_map.get(day)

    # Construct the schtasks command
    command = f"""schtasks /create /tn "{task_name}" /tr "{venv_path} {script_path} {query}" /sc weekly /d {windows_day} /st {time}"""
    print(f"Scheduling task with command: {command}")

    # Run the scheduling command
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Task '{task_name}' scheduled successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Failed to schedule task on Windows: {e}")


def schedule_unix(day, time, query):
    """
    Schedule the digest on Linux/macOS using cron jobs.
    """
    cron = CronTab(user=True)
    script_path = Path(__file__).resolve().parent / "weekly_digest.py"
    venv_path = Path(__file__).resolve().parent.parent / "venv" / "bin" / "python"

    # Map day to cron format (0-6, where 0 = Sunday)
    day_map = {
        "Sunday": 0,
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 3,
        "Thursday": 4,
        "Friday": 5,
        "Saturday": 6,
    }
    cron_day = day_map[day]

    # Extract hours and minutes from time
    hours, minutes = map(int, time.split(":"))

    job = cron.new(command=f"{venv_path} {script_path} {query}", comment=f"WeeklyDigest-{query}-{day}")
    job.setall(f"{minutes} {hours} * * {cron_day}")
    cron.write()

if __name__ == "__main__":
    schedule_digest()
