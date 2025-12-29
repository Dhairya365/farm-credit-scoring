import requests

# API Keys
OPENWEATHERMAP_API_KEY = "e8e2c4cd71ccf2aca8e249967db5e79f"
GEOCODE_API_KEY = "6773080ec4733219117609ptjcf81be"

# Step 1: User Input
def get_user_input():
    print("Enter Soil Health Card Details:")
    nitrogen = float(input("Nitrogen (kg/ha): "))
    phosphorus = float(input("Phosphorus (kg/ha): "))
    potassium = float(input("Potassium (kg/ha): "))
    ph = float(input("pH: "))
    organic_carbon = float(input("Organic Carbon (%): "))

    print("\nEnter Location Details:")
    city = input("Nearest City: ")  # Ask for the nearest city instead of village and district

    farm_size = float(input("\nEnter Farm Size (hectares): "))

    soil_health = {
        "Nitrogen": nitrogen,
        "Phosphorus": phosphorus,
        "Potassium": potassium,
        "pH": ph,
        "Organic_Carbon": organic_carbon
    }

    return soil_health, city, farm_size

# Step 2: Fetch Weather Data
def fetch_weather_data(city_name):
    # Step 1: Get Latitude and Longitude from City Name using Geocode API
    geocode_url = f"https://geocode.maps.co/search?q={city_name}&api_key={GEOCODE_API_KEY}"
    
    try:
        # Fetch latitude and longitude
        geocode_response = requests.get(geocode_url)
        geocode_data = geocode_response.json()
        
        # Check if the city was found
        if not geocode_data:
            print(f"Error: City '{city_name}' not found.")
            return None, None, None
        
        # Extract latitude and longitude
        lat = geocode_data[0]["lat"]
        lon = geocode_data[0]["lon"]
        print(f"Coordinates for {city_name}: Latitude = {lat}, Longitude = {lon}")
        
        # Step 2: Fetch Weather Data using Latitude and Longitude from OpenWeatherMap API
        openweathermap_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
        
        weather_response = requests.get(openweathermap_url)
        weather_data = weather_response.json()
        
        # Check if the weather data was found
        if weather_data.get("cod") != 200:
            print(f"Error: {weather_data.get('message', 'Unknown error')}")
            return None, None, None
        
        # Extract relevant weather data
        weather_condition = weather_data["weather"][0]["main"]  # e.g., Rain, Clear
        temperature = weather_data["main"]["temp"]  # Temperature in Celsius
        humidity = weather_data["main"]["humidity"]
        
        print(f"\nWeather in {city_name}: {weather_condition}, Temperature: {temperature:.1f}°C, Humidity: {humidity}%")
        return weather_condition, temperature, humidity
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None, None, None


def fetch_weather_by_coordinates(lat, lon):
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}&lon={lon}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
        )
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return None, None, None

        return (
            data["weather"][0]["main"],
            data["main"]["temp"],
            data["main"]["humidity"]
        )
    except Exception:
        return None, None, None

# Step 3: Soil Fertility Rating
def calculate_soil_fertility(soil_health):
    ideal_ranges = {
        "Nitrogen": (280, 560),
        "Phosphorus": (10, 25),
        "Potassium": (110, 280),
        "pH": (6.0, 7.5),
        "Organic_Carbon": (0.8, 1.2)
    }
    total_score = 0
    for nutrient, value in soil_health.items():
        low, high = ideal_ranges[nutrient]
        if low <= value <= high:
            total_score += 20  # Full points for ideal range
        elif value < low * 0.8 or value > high * 1.2:
            total_score += 5  # Low points for far outside range
        else:
            total_score += 15  # Partial points for slightly outside range
    return total_score

# Step 4: Weather Risk Adjustment
def get_weather_risk_score(weather_condition):
    if weather_condition in ["Clear", "Clouds"]:
        return 1.0  # Favorable weather
    elif weather_condition in ["Rain", "Drizzle"]:
        return 0.9  # Moderate risk
    elif weather_condition in ["Thunderstorm", "Extreme"]:
        return 0.7  # High risk
    else:
        return 1.0  # Default

# Step 5: Regional Factor Adjustment
def get_regional_factor(city):
    # Example logic: Assign score based on city
    high_productivity_cities = ["CityA", "CityB"]
    medium_productivity_cities = ["CityC", "CityD"]
    
    if city in high_productivity_cities:
        return 1.2
    elif city in medium_productivity_cities:
        return 1.0
    else:
        return 0.8

# Step 6: Farm Size Adjustment
def get_farm_size_score(farm_size):
    if farm_size < 2:
        return 0.8
    elif 2 <= farm_size <= 10:
        return 1.0
    else:
        return 1.2

# Step 7: Credit Score Calculation
def calculate_credit_score(soil_fertility_rating, weather_risk_score, regional_factor_score, farm_size_score):
    credit_score = (soil_fertility_rating / 100) * weather_risk_score * regional_factor_score * farm_size_score * 100
    return min(credit_score, 100)  # Cap at 100