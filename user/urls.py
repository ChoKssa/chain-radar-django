from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path("profile/", views.user_profile, name="user_profile"),
    path('unfollow/<int:pk>/', views.unfollow_crypto, name='unfollow_crypto'),
    path('follow/<int:pk>/', views.follow_crypto, name='follow_crypto'),
]
