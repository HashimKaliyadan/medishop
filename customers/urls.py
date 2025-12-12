from django.urls import path
from . import views

app_name = "customers"

urlpatterns = [
    path("", views.customer_home, name="home"),
    path('account/', views.account, name="account"),
]
