from crypto.models import CryptoCurrency
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from .forms import CustomUserCreationForm
from crypto.models import FollowedCrypto
from django.urls import reverse

def login(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            error_message = "Invalid username or password"

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


@login_required
def user_profile(request):
    user = request.user
    followed_cryptos = user.followed_cryptos.all()

    return render(request, 'user/profile.html', {'user': user, 'followed_cryptos': followed_cryptos})


@login_required
def follow_crypto(request, pk):
    crypto = get_object_or_404(CryptoCurrency, pk=pk)
    FollowedCrypto.objects.get_or_create(user=request.user, crypto=crypto)
    return redirect(request.META.get('HTTP_REFERER') or reverse('crypto_list'))

@login_required
def unfollow_crypto(request, pk):
    if request.method == 'POST':
        crypto = get_object_or_404(CryptoCurrency, pk=pk)
        FollowedCrypto.objects.filter(user=request.user, crypto=crypto).delete()
    return redirect(request.META.get('HTTP_REFERER') or reverse('crypto_list'))
