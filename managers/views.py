from django.shortcuts import render
from main.decorators import allow_manager
from managers.models import Category, Medicine
from customers.models import Order

@allow_manager
def dashboard(request):
    context = {
        "total_categories": Category.objects.count(),
        "total_medicines": Medicine.objects.count(),
        "total_orders": Order.objects.count(),
    }
    return render(request, "managers/dashboard.html", context)
