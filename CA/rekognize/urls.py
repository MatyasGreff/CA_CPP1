from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'), #This is the object rekognition page
    path('celebrity/', views.celebrity, name='celebrity'),
    path('about/', views.about, name='about'),
    path('allimages/', views.allimages, name='allimages'),
    path('viewimage/<str:pk>/', views.viewimage, name='viewimage'),
]