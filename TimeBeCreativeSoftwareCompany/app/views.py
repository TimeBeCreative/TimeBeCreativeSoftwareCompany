from django.http import HttpResponse
from django.shortcuts import render

from TimeBeCreativeSoftwareCompany.settings import EMAIL_HOST_USER
from .forms import ContactForm
from django.core.mail import send_mail


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

            send_mail(
                f"Message from {name} <{email}>",
                message,
                EMAIL_HOST_USER,
                ["cherevatenkoviktoriya@gmail.com"],
               # headers={'Reply-To': email},
                fail_silently = False,
                

            )

            send_mail(
                f"Дякуємо за звернення до TimeBeCreativeSoftwareCompany",
                f"{name},\n\nДякуємо за ваше повідомлення, ми розглянемо його і відповімо, як тільки буде змога. Лист до нашої інноваційної та потужної компанії гарантує вам крок до успіху, адже ми перетворюємо ідеї на програмні рішення.\n\nЗ повагою,\nкоманда TimeBeCreativeSoftwareCompany",
                EMAIL_HOST_USER,
                [email],
                fail_silently = False,
            )

            return render(request, "app/contact.html", {"form": ContactForm(), "success": True})
    else:
        form = ContactForm()


    return render(request, "app/contact.html", {"form": form})


