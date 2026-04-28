"""
Job Listing Scraper using BeautifulSoup (Stable Site)
Author: Shubhransu
Output: jobs_data_bs4.csv
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

URL = "https://realpython.github.io/fake-jobs/"


def fetch_page():
    response = requests.get(URL)
    response.raise_for_status()
    return response.text


def parse_jobs(html):
    soup = BeautifulSoup(html, "html.parser")
    job_cards = soup.find_all("div", class_="card-content")

    jobs = []

    for job in job_cards:
        title = job.find("h2", class_="title")
        company = job.find("h3", class_="company")
        location = job.find("p", class_="location")

        # ✅ FIXED URL extraction
        link_tag = job.find("a", href=True)
        url = "https://realpython.github.io" + link_tag["href"] if link_tag else ""

        jobs.append({
            "job_title": title.get_text(strip=True) if title else "",
            "company": company.get_text(strip=True) if company else "",
            "location": location.get_text(strip=True) if location else "",
            "url": url,
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return jobs


def run_scraper():
    html = fetch_page()
    jobs = parse_jobs(html)
    df = pd.DataFrame(jobs)
    return df


def save_to_csv(df):
    df.to_csv("jobs_data_bs4.csv", index=False, encoding="utf-8-sig")
    print(f"Saved {len(df)} jobs")


if __name__ == "__main__":
    df = run_scraper()
    save_to_csv(df)
    print(df.head())