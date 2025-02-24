import requests
from bs4 import BeautifulSoup
import phonenumbers
from phonenumbers import geocoder, carrier

def search_phone_number(phone_number):
    query = f"{phone_number} profile"
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    # Debugging: Check response status and content
    print(f"Response Status: {response.status_code}")
    print(f"Response Content: {response.text[:500]}")  # Print first 500 characters of the response

    if response.status_code != 200:
        print(f"Failed to retrieve search results. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for g in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd'):
        try:
            title = g.get_text()
            link = g.find_previous('a')['href']
            results.append({'title': title, 'link': link})
        except Exception as e:
            print(f"Error parsing result: {e}")
    
    return results

def parse_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        location = geocoder.description_for_number(parsed_number, 'en')
        service_provider = carrier.name_for_number(parsed_number, 'en')
        return location, service_provider
    except phonenumbers.phonenumberutil.NumberParseException:
        print("Invalid phone number format.")
        return None, None

def main():
    phone_number = input("Enter the phone number (with country code): ")
    location, service_provider = parse_phone_number(phone_number)
    
    if location and service_provider:
        print(f"Location: {location}")
        print(f"Service Provider: {service_provider}")

        print("\nSearching online for profiles and reports...")
        results = search_phone_number(phone_number)
        for i, result in enumerate(results, start=1):
            print(f"\nResult {i}:")
            print(f"Title: {result['title']}")
            print(f"Link: {result['link']}")
    else:
        print("Unable to retrieve information for the provided phone number.")

if __name__ == "__main__":
    main()
