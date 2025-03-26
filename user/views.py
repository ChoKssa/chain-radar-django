from django.shortcuts import render

def login(request):
    context = {}
    return render(request, "user/login.html", context)

def signup(request):
    context = {}
    return render(request, "user/signup.html", context)
