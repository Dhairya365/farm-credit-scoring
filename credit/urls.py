from django.urls import path
from . import views

urlpatterns = [
    # path('calculate/', views.calculate_credit, name='calculate_credit'),
    path('', views.index, name='index'),
    path('api/calculate/', views.calculate_credit_api, name='calculate_credit_api'),
]
