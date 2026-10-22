import requests

# --- CONFIGURATION ---
BOT_TOKEN = "8859960091:AAG0tneOdw7MixiWyg_KB7xSUuLJsJBnUyk"
CHAT_ID = "698119277"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Telegram alert sent successfully.")
    else:
        print(f"Failed to send alert: {response.text}")

def search_medical_jobs():
    # Replace this mock data with actual scraping logic for Bayt, LinkedIn, or Indeed
    new_jobs = [
        {
            "title": "General Physician (GP)", 
            "company": "Private Clinic",
            "location": "Safwa, Eastern Province", 
            "link": "https://example.com/apply"
        }
    ]

    if new_jobs:
        alert_text = "🏥 <b>New Medical Job Alerts</b>\n\n"
        for job in new_jobs:
            alert_text += f"👨‍⚕️ <b>{job['title']}</b>\n"
            alert_text += f"🏢 <i>{job['company']}</i>\n"
            alert_text += f"📍 {job['location']}\n"
            alert_text += f"🔗 <a href='{job['link']}'>Apply Here</a>\n\n"
            
        send_telegram_alert(alert_text)
    else:
        print("No new jobs found.")

if __name__ == "__main__":
    search_medical_jobs()
