from django.http import HttpResponse
from django.shortcuts import render

from TimeBeCreativeSoftwareCompany.settings import EMAIL_HOST_USER
from .forms import ContactForm
from django.core.mail import send_mail
import threading

def send_email_async(subject, message, from_email, recipient_list):
    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        print("EMAIL SENT SUCCESSFULLY")
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


            thread1 = threading.Thread(target=send_email_async, args=(
                f"Message from {name} <{email}>",
                message,    
                EMAIL_HOST_USER,
                ["cherevatenkoviktoriya@gmail.com"]

            )
            )
            thread1.daemon = True
            thread1.start()
            
            thread2 = threading.Thread(target=send_email_async, args=(
                f"Дякуємо за звернення до TimeBeCreativeSoftwareCompany",
                f"{name},\n\nДякуємо за ваше повідомлення, ми розглянемо його і відповімо, як тільки буде змога. Лист до нашої інноваційної та потужної компанії гарантує вам крок до успіху, адже ми перетворюємо ідеї на програмні рішення.\n\nЗ повагою,\nкоманда TimeBeCreativeSoftwareCompany",
                EMAIL_HOST_USER,
                [email],
                )
            )
            thread2.daemon = True
            thread2.start()
            

            return render(request, "app/contact.html", {"form": ContactForm(), "success": True})
    else:
        form = ContactForm()


    return render(request, "app/contact.html", {"form": form})


