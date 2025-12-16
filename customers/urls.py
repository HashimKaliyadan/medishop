from django.urls import path
from . import views

app_name = "customers"

urlpatterns = [
    path("", views.customer_home, name="home"),
    path("categories/", views.category_list, name="category-list"),
    path("categories/<slug:slug>/", views.medicine_list_by_category, name="medicine-by-category"),
    path("medicines/", views.all_medicines, name="medicine-list"),
    path("medicine/<slug:slug>/", views.medicine_detail, name="medicine-detail"),
]
