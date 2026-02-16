import requests

def test_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=j1"
        print(f"Testing weather API for {city}...")
        response = requests.get(url, timeout=5)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            temp = current['temp_C']
            wind_speed = current['windspeedKmph']
            wind_dir = current['winddir16Point']
            weather_desc = current['weatherDesc'][0]['value']
            
            print(f"\nWeather: {weather_desc}")
            print(f"Temperature: {temp}°C")
            print(f"Wind: {wind_speed} km/h {wind_dir}")
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

test_weather("Pune")
