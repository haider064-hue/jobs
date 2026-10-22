import requests
import os
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
BOT_TOKEN = "8859960091:AAG0tneOdw7MixiWyg_KB7xSUuLJsJBnUyk"
CHAT_ID = "698119277" 

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    requests.post(url, json=payload)

def scrape_bayt():
    new_jobs = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    url = "https://www.bayt.com/en/saudi-arabia/jobs/medical-healthcare-jobs/?job_title=physician&job_title=resident"
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        job_cards = soup.find_all('li', class_='has-pointer-d')
        
        for card in job_cards[:5]:
            title_elem = card.find('h2')
            company_elem = card.find('b', class_='jb-company')
            loc_elem = card.find('span', class_='jb-loc')
            
            if title_elem:
                title = title_elem.text.strip()
                link = "https://www.bayt.com" + title_elem.find('a')['href']
                company = company_elem.text.strip() if company_elem else "Private Facility"
                location = loc_elem.text.strip() if loc_elem else "Saudi Arabia"
                
                if any(loc in location.lower() for loc in ['riyadh', 'eastern province', 'dammam', 'khobar', 'safwa']):
                    new_jobs.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "link": link
                    })
    except Exception as e:
        print(f"Bayt Scraper Error: {e}")
        
    return new_jobs

def get_protected_portals():
    new_jobs = []
    rapid_api_key = os.getenv("RAPID_API_KEY")
    
    if not rapid_api_key:
        print("Error: RapidAPI key not found. Did you add it to GitHub Secrets?")
        return new_jobs

    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    queries = [
        "General Physician KFSH&RC in Riyadh",
        "General Physician KFSH&RC in Eastern Province",
        "Resident KKUH in Riyadh"
    ]

    for query in queries:
        querystring = {"query": query, "page": "1", "num_pages": "1"}
        try:
            response = requests.get(url, headers=headers, params=querystring, timeout=15)
            data = response.json()
            
            if response.status_code == 200 and data.get("data"):
                for job in data["data"][:3]:
                    new_jobs.append({
                        "title": job.get("job_title", "Medical Job"),
                        "company": job.get("employer_name", "Hospital"),
                        "location": f"{job.get('job_city', '')}, {job.get('job_state', '')}",
                        "link": job.get("job_apply_link", "")
                    })
            else:
                print(f"No results for '{query}'")
        except Exception as e:
            print(f"JSearch API Error for '{query}': {e}")

    return new_jobs

def search_medical_jobs():
    all_jobs = []
    print("Scraping Bayt...")
    all_jobs.extend(scrape_bayt())
    print("Fetching APIs for KFSH&RC, KKUH, and LinkedIn...")
    all_jobs.extend(get_protected_portals())

    if all_jobs:
        alert_text = "🏥 <b>New Medical Job Alerts</b>\n\n"
        for job in all_jobs:
            alert_text += f"👨‍⚕️ <b>{job['title']}</b>\n"
            alert_text += f"🏢 <i>{job['company']}</i>\n"
            alert_text += f"📍 {job['location']}\n"
            alert_text += f"🔗 <a href='{job['link']}'>Apply Here</a>\n\n"
            
        send_telegram_alert(alert_text)
        print("Alerts sent.")
    else:
        print("No new matching jobs found today.")

if __name__ == "__main__":
    search_medical_jobs()
