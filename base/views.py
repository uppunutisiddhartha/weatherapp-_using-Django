from django.shortcuts import render
import requests

def index(request):
    weather_data = None
    error_message = None

    if request.method == "POST":
        city = request.POST.get('city')  
        if city:  
            api_key = "9fff33045ee77b36cde13aaa3ee76e14"
            api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    data = response.json()
                    weather_data = {
                        "city": city,
                        "temperature": data["main"]["temp"],
                        "description": data["weather"][0]["description"],
                        "icon": data["weather"][0]["icon"]
                    }
                else:
                    error_message = "City not found. Try again!"
            except requests.exceptions.RequestException as e:
                error_message = "An error occurred while fetching the weather data. Please try again later."
        else:
            error_message = "Please enter a city name."

    return render(request, "index.html", {"weather": weather_data, "error": error_message})