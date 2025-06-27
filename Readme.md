Ran tool
Read file: main.ipynb
Read file: scraper.py
Bu repoda LinkedIn iş ilanlarından belirli pozisyonlar için veri çekip, bu ilanlardaki yetkinlikleri analiz eden bir Python uygulaması var. Ana dosya `main.ipynb` ve veri çekme işlemi `scraper.py` ile yapılıyor.

İşte İngilizce bir README taslağı:

---

# LinkedIn Job Skills Scraper & Analyzer

## Overview
This project scrapes job postings from LinkedIn for selected job titles and locations, then analyzes the most in-demand skills and trends in the job market. It is designed to help job seekers understand which skills are most requested for roles like "AI Engineer", "Machine Learning Engineer", and similar positions in Turkey.

## Features
- Scrapes job postings from LinkedIn using custom search titles and locations.
- Extracts job descriptions, company names, locations, and posting dates.
- Uses semantic similarity to filter relevant job postings.
- Analyzes and aggregates the most requested skills and trends.
- Provides actionable recommendations for job seekers.

## How It Works
1. **scraper.py**: Fetches job postings from LinkedIn, extracts details, and filters by semantic similarity.
2. **main.ipynb**: Configures job titles/locations, runs the scraper, and performs data analysis on the collected postings.

## Requirements
- Python 3.8+
- Packages: `requests`, `beautifulsoup4`, `pandas`, `sentence-transformers`, `fuzzywuzzy`, `tqdm`, `openai`, `tiktoken`

## Usage
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Edit job titles and locations in `main.ipynb`.
3. Run `main.ipynb` to scrape data and analyze skills.

## Notes
- For educational/research use only. Scraping LinkedIn may violate their terms of service.
- The script uses semantic similarity to ensure relevant job matches.

---
