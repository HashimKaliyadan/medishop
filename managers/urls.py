from django.urls import path
from . import views

app_name = "managers"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("medicines/", views.medicine_list, name="medicine-list"),
    path("medicines/add/", views.medicine_create, name="medicine-add"),
    path("medicines/<int:pk>/edit/", views.medicine_edit, name="medicine-edit"),
    path("medicines/<int:pk>/delete/", views.medicine_delete, name="medicine-delete"),
    path("categories/", views.category_list, name="category-list"),
    path("categories/add/", views.category_create, name="category-add"),
    path("categories/<int:pk>/edit/", views.category_edit, name="category-edit"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category-delete"),
]
