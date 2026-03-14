from django.http import HttpResponse
from django.shortcuts import render
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
                f"Message from {name}",
                message,
                email,
                ["cherevatenkoviktoriya@gmail.com"],
            )

            return render(request, "app/contact.html", {"form": ContactForm(), "success": True})
    else:
        form = ContactForm()

    return render(request, "app/contact.html", {"form": form})
