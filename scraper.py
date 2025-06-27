import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from fuzzywuzzy import fuzz
from tqdm import tqdm

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

model = SentenceTransformer('all-MiniLM-L6-v2')

per_page = 50
total_scraped_jobs = 0  # Genel toplam

def get_job_description_and_posted_date(job_url):
    try:
        response = requests.get(job_url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Detaya erişim başarısız: {job_url}")
            return None, None

        soup = BeautifulSoup(response.text, "html.parser")
        description_div = soup.find("div", class_="show-more-less-html__markup")
        job_description = description_div.get_text(separator="\n", strip=True) if description_div else None

        # Posted Date çekimi
        posted_date_span = soup.find("span", class_="posted-time-ago__text")
        posted_date = posted_date_span.get_text(strip=True) if posted_date_span else None

        return job_description, posted_date

    except Exception as e:
        print(f"Detay çekim hatası: {e}")
        return None, None

def scrape_jobs(search_title, location, max_results=50):
    all_jobs = []
    seen_job_links = set()

    start = 0
    total_fetched = 0

    while total_fetched < max_results:
        title_encoded = urllib.parse.quote(search_title)
        location_encoded = urllib.parse.quote(location)
        url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={title_encoded}&location={location_encoded}&start={start}"

        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200 or not response.text.strip():
            print(f"[{search_title} - {location}] Daha fazla ilan bulunamadı.")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("li")

        if not job_cards:
            print(f"[{search_title} - {location}] İlan kartı bulunamadı.")
            break
        
        job_count = 0
        for job in tqdm(job_cards, desc="Fetching job cards", position=1, leave=False,
                        bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}]"):
        #for job in job_cards:
            try:
                job_title = job.find("h3").get_text(strip=True)
                company_name = job.find("h4").get_text(strip=True)
                job_location = job.find("span", class_="job-search-card__location").get_text(strip=True)
                job_link = job.find("a", class_="base-card__full-link")['href']

                if job_link in seen_job_links:
                    continue
                seen_job_links.add(job_link)

                embedding1 = model.encode(search_title, convert_to_tensor=True)
                embedding2 = model.encode(job_title, convert_to_tensor=True)
                similarity = util.cos_sim(embedding1, embedding2).item() * 100

                if similarity < 70:
                    continue

                job_description, posted_date = get_job_description_and_posted_date(job_link)

                job_data = {
                    "Search Title": search_title,
                    "Job Title": job_title,
                    "Similarity": similarity,
                    "Search Location": location,
                    "Company": company_name,
                    "Job Location": job_location,
                    "Job Link": job_link,
                    "Posted Date": posted_date,
                    "Description": job_description
                }
                all_jobs.append(job_data)

                total_fetched += 1
                job_count += 1
                if total_fetched >= max_results:
                    break
                
                time.sleep(1)

            except Exception as e:
                print(f"Hata: {e}")
                continue

        start += per_page
        time.sleep(1)

    #print(f"[{search_title} - {location}] ✅ {len(all_jobs)} job post scraped.")
    return pd.DataFrame(all_jobs)
