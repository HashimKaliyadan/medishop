from django.shortcuts import render, get_object_or_404
from managers.models import Category, Medicine

def customer_home(request):
    return render(request, "customers/home.html")

def category_list(request):
    categories = Category.objects.filter(is_active=True).order_by("name")
    return render(request, "customers/category_list.html", {
        "categories": categories
    })

def medicine_list_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    medicines = Medicine.objects.filter(
        category=category,
        in_stock=True
    ).order_by("name")

    return render(request, "customers/medicine_list.html", {
        "category": category,
        "medicines": medicines,
    })

def all_medicines(request):
    medicines = Medicine.objects.filter(in_stock=True).order_by("name")
    return render(request, "customers/all_medicines.html", {
        "medicines": medicines
    })

def medicine_detail(request, slug):
    medicine = get_object_or_404(Medicine, slug=slug, in_stock=True)
    return render(request, "customers/medicine_detail.html", {
        "medicine": medicine
    })