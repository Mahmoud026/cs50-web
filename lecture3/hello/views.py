from django.http import HttpResponse  # type: ignore
from django.shortcuts import render  # type: ignore

# View for the home page; returns a greeting message
def index(request):
    return render(request, "hello/index.html")

# View for the 'mahmoud' page; returns a statement about web development
def mahmoud(request):
    return HttpResponse("I am the pioneer of a new way of web development by 2026.")

# View for the 'dream' page; returns a personal aspiration
def dream(request):
    return HttpResponse("I want to be a good developer and a good person.")

# View for personalized greeting; takes a name from the URL and returns a capitalized greeting
def greet(request, name):
    # Render the 'greet.html' template, passing the capitalized name as context
    return render(request, "hello/greet.html", {
        "name": name.capitalize()  # Capitalize the first letter of the provided name
    })