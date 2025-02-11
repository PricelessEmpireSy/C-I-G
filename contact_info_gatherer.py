import requests
from bs4 import BeautifulSoup
import phonenumbers
from phonenumbers import geocoder, carrier

def search_phone_number(phone_number):
    query = f"{phone_number} scam report"
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for g in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd'):
        title = g.get_text()
        link = g.find_previous('a')['href']
        results.append({'title': title, 'link': link})
    
    return results

def parse_phone_number(phone_number):
    parsed_number = phonenumbers.parse(phone_number, None)
    location = geocoder.description_for_number(parsed_number, 'en')
    service_provider = carrier.name_for_number(parsed_number, 'en')
    return location, service_provider

def main():
    phone_number = input("Enter the phone number (with country code): ")
    location, service_provider = parse_phone_number(phone_number)
    print(f"Location: {location}")
    print(f"Service Provider: {service_provider}")

    print("\nSearching online for scam reports...")
    results = search_phone_number(phone_number)
    for i, result in enumerate(results, start=1):
        print(f"\nResult {i}:")
        print(f"Title: {result['title']}")
        print(f"Link: {result['link']}")

if __name__ == "__main__":
    main()

