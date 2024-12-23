import requests
import openai
from openai import OpenAI
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from weeklyresearchdigest.config import (
    EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT,
    SMTP_SERVER, SMTP_PORT, OPENAI_API_KEY, DEFAULT_QUERY
)
# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

def fetch_biorxiv_papers(query, max_results=10, days=20):
    """
    Fetch papers from bioRxiv API within the last `days` days and filter by query.
    """
    # Calculate date range
    today = datetime.now()
    from_date = (today - timedelta(days=days)).strftime("%Y-%m-%d")
    to_date = today.strftime("%Y-%m-%d")

    url = f"https://api.biorxiv.org/details/biorxiv/{from_date}/{to_date}"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Extract and filter papers based on query
        papers = []
        for paper in data["collection"]:
            if query.lower() in paper["title"].lower() or query.lower() in paper["abstract"].lower():
                papers.append({
                    "title": paper["title"],
                    "authors": paper["authors"],
                    "abstract": paper["abstract"],
                    "link": f"https://doi.org/{paper['doi']}"
                })

            if len(papers) >= max_results:
                break

        return papers
    except Exception as e:
        print(f"Error fetching data from bioRxiv API: {e}")
        return []

def parse_biorxiv_papers(data):
    """
    Parse the response from bioRxiv and extract titles, authors, abstracts, and DOIs.
    """
    papers = []
    for paper in data.get("results", []):
        papers.append({
            "title": paper["title"],
            "authors": paper["authors"],
            "abstract": paper["abstract"],
            "link": f"https://doi.org/{paper['doi']}"  # Construct DOI link
        })
    return papers

# Function to fetch papers from arXiv
def fetch_arxiv_papers(query, max_results=5):
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    response = requests.get(ARXIV_API_URL, params=params, timeout=30)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# Parse and structure the data
def parse_papers(data):
    papers = []
    if data:
        entries = data.split("<entry>")
        for entry in entries[1:]:
            title = extract_tag(entry, "title")
            authors = [a.strip() for a in extract_tag(entry, "author").split(",")]
            abstract = extract_tag(entry, "summary")
            link = extract_tag(entry, "id")
            if title and authors and abstract and link:
                papers.append({
                    "title": title.strip(),
                    "authors": authors,
                    "abstract": abstract.strip(),
                    "link": link.strip(),
                })
    return papers

def extract_tag(text, tag):
    try:
        start = text.find(f"<{tag}>") + len(tag) + 2
        end = text.find(f"</{tag}>")
        return text[start:end]
    except:
        return None

# Function to generate summaries using OpenAI
def generate_summary(papers):
    # Construct the message for ChatGPT
    messages = [
        {"role": "system", "content": "You are a helpful assistant summarizing academic papers."},
        {"role": "user", "content": "Summarize the following academic papers and relate them to each other and the broader literature:\n\n"}
    ]

    # Add each paper to the user message
    for paper in papers:
        messages[-1]["content"] += f"Title: {paper['title']}\n"
        messages[-1]["content"] += f"Authors: {', '.join(paper['authors'])}\n"
        messages[-1]["content"] += f"Abstract: {paper['abstract']}\n\n"
    
    messages[-1]["content"] += "Provide an overarching narrative about how these papers relate to each other and to the broader literature:\n"
    try:
        client = OpenAI(
            api_key=openai.api_key,  # This is the default and can be omitted
        )

        response = client.chat.completions.create(
            messages=messages,
            model="gpt-4o",
            temperature=0.7,
        )
        # # Use the ChatCompletion API
        # response = openai.ChatCompletion.create(
        #     model="gpt-4",
        #     messages=messages,
        #     temperature=0.7,
        #     max_tokens=1000
        # )
        # print(response)
        return response.choices[0].message.content
        # return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "Error generating summary."


# Function to send an email
def send_email(subject, body, recipient):
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)

        msg = MIMEMultipart("alternative")
        msg["Query"] == DEFAULT_QUERY
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = recipient

        msg.attach(MIMEText(body, "html"))

        server.sendmail(EMAIL_SENDER, recipient, msg.as_string())

        # Print to log
        # Open the .log file in append mode
        with open('D://WeeklyDigest//weekly_research_digest//logs//digest.log', "a") as log_file:

            # Get the current date and time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Add a timestamped comment to the LaTeX file
            log_file.write(f"% Log entry added on {current_time}\n")
            log_file.write("\n This is a new log entry.\n")
            log_file.write(body)

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

# Main function for the weekly digest
def run_weekly_digest():
    # raw_data = fetch_arxiv_papers(QUERY, max_results=5)
    # papers = parse_papers(raw_data)
    # papers = fetch_biorxiv_papers(QUERY, max_results=5)
    papers = fetch_biorxiv_papers(DEFAULT_QUERY, max_results=10, days=30)
    if papers:
        summary = generate_summary(papers)

        email_body = f"<h1>Weekly Digest</h1>\n<p>{summary}</p>\n<hr>\n"
        for paper in papers:
            email_body += f"<h3>{paper['title']}</h3>\n"
            email_body += f"<h3>{paper['authors']}</h3>\n"
            email_body += f"<p>{paper['abstract']}</p>\n<hr>\n"

        send_email("Weekly Research Digest", email_body, EMAIL_RECIPIENT)
    else:
        print("No papers found for this week's digest.")
