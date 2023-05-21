from django.contrib import admin
from django.urls import path, include
from frontend import views

urlpatterns = [
    path('', views.index, name='index'),
    path('flight_detail/<int:id_flight>/', views.flight_detail, name='flight_detail'),
    path('user_page/<str:username>/', views.user_page),
]
