from django.shortcuts import render
import requests
from django.core.mail import send_mail
from .models import Suggestion
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

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
    if request.method == 'POST':
        email = request.POST['email']
        title = request.POST['title']
        suggestion_text = request.POST['suggestion']

        # Save to database
        Suggestion.objects.create(
            email=email,
            title=title,
            suggestion=suggestion_text
        )

        # Email content
        subject = 'Thanks for Your Valuable Suggestion!'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [email]

        text_content = f"Thank you for your suggestion titled: {title}."

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <style>
            .email-container {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                padding: 20px;
                color: #333;
            }}
            .content {{
                background-color: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.05);
            }}
            h2 {{
                color: #076089;
            }}
            p {{
                font-size: 16px;
                line-height: 1.6;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 14px;
                color: #888;
            }}
          </style>
        </head>
        <body>
          <div class="email-container">
            <div class="content">
              <h2>Thank You!</h2>
              <p>Hi ,</p>
              <p>Thank you for sharing your suggestion titled: <strong>{title}</strong>.</p>
              <p>I truly appreciate your time and feedback. Your input helps me improve this project and make it more useful for everyone.</p>
              <p>If you have more ideas or feedback, feel free to reach out again!</p>
              <p>Best regards,<br>
              <strong>Siddhartha Uppunuti</strong><br>
              Developer | Django</p>
              <div class="footer">
                <p>This is an automated message. Please do not reply directly.</p>
              </div>
            </div>
          </div>
        </body>
        </html>
        """

        # Send HTML email
        email_message = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()

        return render(request, 'index.html', {'success': True})

    return render(request, 'index.html')