import os
import subprocess
import sys
from dotenv import dotenv_values, set_key
from weeklyresearchdigest.config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT, OPENAI_API_KEY, DEFAULT_QUERY
from weeklyresearchdigest.digest_logic import run_weekly_digest


CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.env")

def check_and_populate_config():
    """
    Check if required variables in config.env are missing or empty and prompt the user to populate them.
    """
    from dotenv import dotenv_values, set_key

    config = dotenv_values(CONFIG_FILE)
    required_vars = {
        "EMAIL_SENDER": "Email address of the sender",
        "EMAIL_PASSWORD": "Password for the email account",
        "EMAIL_RECIPIENT": "Email address of the recipient",
        "OPENAI_API_KEY": "OpenAI API key",
        "SMTP_SERVER": "SMTP server (default: smtp.gmail.com)",
        "SMTP_PORT": "SMTP port (default: 587)",
        "DEFAULT_QUERY": "Default query for research digest",
    }

    missing_vars = {key: prompt for key, prompt in required_vars.items() if not config.get(key)}

    if missing_vars:
        print("Some required variables in config.env are missing or empty.")
        for var, prompt in missing_vars.items():
            if not os.isatty(0):  # If running in a non-interactive mode
                print(f"Error: {var} is missing in config.env. Please populate it.")
                return False
            new_value = input(f"{prompt} ({var}): ").strip()
            if new_value:
                set_key(CONFIG_FILE, var, new_value)
                print(f"Set {var} = {new_value}")
            else:
                print(f"Warning: {var} is still missing.")

        print("Config.env validation complete.")
    else:
        print("All required environment variables are set.")
    return True


# Main function
def main():
    parser = argparse.ArgumentParser(description="Run the Weekly Research Digest.")
    parser.add_argument(
        "query",
        nargs="?",
        default=DEFAULT_QUERY,
        help="The query term to fetch research papers for (default: from config)."
    )
    args = parser.parse_args()

    query = args.query
    print(f"Running the Weekly Research Digest for query: {query}")
    try:
        # Check and populate missing variables in config.env
        check_and_populate_config()
        # Import and run the digest logic
        # from weeklyresearchdigest.digest_logic import run_weekly_digest
        print("Running the weekly digest script...")
        run_weekly_digest(query)
        print("Weekly digest completed.")
    except Exception as e:
        print(f"An error occurred during execution: {e}")
    finally:
        # Ensure clean exit
        sys.exit(0)
        # os._exit(0)

if __name__ == "__main__":
    main()
