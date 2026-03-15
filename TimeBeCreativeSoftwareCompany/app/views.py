from django.http import HttpResponse
from django.shortcuts import render

from TimeBeCreativeSoftwareCompany.settings import EMAIL_HOST_USER
from .forms import ContactForm
from django.core.mail import send_mail
import threading
import os
import resend

resend.api_key = os.environ.get('RESEND_API_KEY')

def send_email_resend(subject, message, to_email):
    try:
        r = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": to_email,
            "subject": subject,
            "html": f"<p>{message}</p>"
        })
        print("EMAIL SENT SUCCESSFULLY:", to_email)
        return r
    except Exception as e:
        print("EMAIL SENDING ERROR:", e)



# Create your views here.

def index(request):
    return render(request, "app/index.html")

def about(request):
    return render(request, "app/about.html")

def services(request):
    return render(request, "app/services.html")

def contact(request):
    form = ContactForm()
    return render(request, "app/contact.html", {"form": form})

def submit_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            # Лист до тебе
            send_email_resend(
                f"Message from {name} <{email}>",
                message,
                "cherevatenkoviktoriya@gmail.com"
            )

            # Лист клієнту
            send_email_resend(  
                f"Дякуємо за звернення до TimeBeCreativeSoftwareCompany",
                f"{name},<br><br>якуємо за ваше повідомлення, ми розглянемо його і відповімо, як тільки буде змога. Лист до нашої інноваційної та потужної компанії гарантує вам крок до успіху, адже ми перетворюємо ідеї на програмні рішення.<br><br>З повагою,<br>команда TimeBeCreativeSoftwareCompany",
                email
            )

            return render(request, "app/contact.html", {"form": ContactForm(), "success": True})

    else:
        form = ContactForm()

    return render(request, "app/contact.html", {"form": form})