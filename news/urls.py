from django.urls import path

from . import views

urlpatterns = [
    path("articles/", views.article_list, name="article_list"),
    path("article_create/", views.article_create, name="article_create"),
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
    path('articles/<int:pk>/edit/', views.article_update, name='article_update'),
    path('articles/<int:pk>/delete/', views.article_delete, name='article_delete'),
]
