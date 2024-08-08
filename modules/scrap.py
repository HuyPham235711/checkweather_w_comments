# importing library
import requests
from bs4 import BeautifulSoup
import sys
import io

# Set the default encoding to utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_ip_location():
    response = requests.get('https://ipinfo.io/json')
    data = response.json()
    return data

def get_weather():
    #get location
    location_ip = get_ip_location()
    city = location_ip.get('city', 'Unknown')

    # creating url and requests instance
    url = "https://www.google.com/search?q="+"weather"+city
    html_request_check = requests.get(url)

    if html_request_check.status_code == 200:
        # Parse the HTML content
        html = requests.get(url).content
        
        try:
            # getting raw data
            soup = BeautifulSoup(html, 'html.parser')
            temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
            str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

            # formatting data
            data = str.split('\n')
            time = data[0]
            sky = data[1]

            # store data
            weather_info = {
                "city": city,
                "temp": temp,
                "time": time,
                "sky": sky
            }
            
            return weather_info
        except:
            return None
    else:
        return None