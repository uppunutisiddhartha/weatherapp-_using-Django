from django.shortcuts import render
import requests
from django.core.mail import send_mail
from .models import Suggestion
from django.conf import settings

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

#how i developed this

def about(request):
    return render(request,"about.html")

def suggestion(request):
    if request.method=='POST':
        email=request.POST['email']
        title=request.POST['title']
        suggestion=request.POST['suggestion']


        Suggestion.objects.create(
            email=email,
            title=title,
            suggestion=suggestion
        )

        # Send confirmation email
        subject = 'Thank You for Your Suggestion!'
        message = f"""
        Dear Contributor,

        Thank you so much for taking the time to share your suggestion titled: "{title}".

        We genuinely appreciate your input and value your efforts in helping us improve the E.Book Community platform. Every suggestion we receive brings us closer to creating a better experience for all our users.

        If you have more ideas in the future, feel free to reach out anytime!

        Warm regards,  
        Siddhartha Uppunuti  

        """
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        return render(request, 'index.html')


    return render(request, 'index.html')
    return render(request,"index.html")