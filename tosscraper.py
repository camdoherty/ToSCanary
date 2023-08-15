# Import modules
import requests
from bs4 import BeautifulSoup
import sqlite3
import gpt4

# Define online platforms
platforms = ["x.com", "instagram.com"]

# Connect to database
conn = sqlite3.connect("tos.db")
cur = conn.cursor()

# Loop through online platforms
for platform in platforms:
    # Make a request to terms of services page
    url = "https://" + platform + "/terms"
    response = requests.get(url)
    
    # Parse the response
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract date and content
    date = soup.find("p", class_="date").text
    content = soup.find("div", class_="content").text
    
    # Summarize content using gpt4's API
    summary = gpt4.summarize(content)
    
    # Highlight potential privacy or data usage concerns in content
    highlights = gpt4.highlight(content)
    
    # Rank platform on a scale of 1-10 for privacy and other data usage factors
    rank = gpt4.rank(content)
    
    # Insert or update terms of services in database
    cur.execute("INSERT OR REPLACE INTO tos (platform, url, date, content, summary, highlights, rank) VALUES (?, ?, ?, ?, ?, ?, ?)", (platform, url, date, content, summary, highlights, rank))
    
# Close database connection
conn.commit()
conn.close()
