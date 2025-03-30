from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import CustomUserCreationForm
from .models import CustomUser

def login(request):
    error_message = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = None

        if user:
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('/')
            else:
                error_message = "Invalid password"
        else:
            error_message = "User not found"

    return render(request, 'user/login.html', { 'error_message': error_message })

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'user/signup.html', {'form': form})
