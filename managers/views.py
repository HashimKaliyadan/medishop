from django.shortcuts import render , redirect , get_object_or_404
from main.decorators import allow_manager
from managers.models import Category, Medicine
from customers.models import Order
from .forms import MedicineForm, CategoryForm
from django.utils.timezone import now
from django.db.models import Sum


@allow_manager
def dashboard(request):
    today = now().date()

    total_categories = Category.objects.count()
    total_medicines = Medicine.objects.count()
    total_orders = Order.objects.count()

    today_orders = Order.objects.filter(created_at__date=today).count()
    today_revenue = (
        Order.objects.filter(created_at__date=today)
        .aggregate(total=Sum("total"))["total"] or 0
    )

    context = {
        "total_categories": total_categories,
        "total_medicines": total_medicines,
        "total_orders": total_orders,
        "today_orders": today_orders,
        "today_revenue": today_revenue,
    }

    return render(request, "managers/dashboard.html", context)

@allow_manager
def medicine_list(request):
    medicines = Medicine.objects.select_related("category").order_by("name")
    return render(request, "managers/medicine_list.html", {
        "medicines": medicines
    })

@allow_manager
def medicine_create(request):
    if request.method == "POST":
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("managers:medicine-list")
    else:
        form = MedicineForm()

    return render(request, "managers/medicine_form.html", {"form": form})

@allow_manager
def medicine_edit(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)

    if request.method == "POST":
        form = MedicineForm(request.POST, request.FILES, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect("managers:medicine-list")
    else:
        form = MedicineForm(instance=medicine)

    return render(request, "managers/medicine_form.html", {
        "form": form,
        "is_edit": True,
    })


@allow_manager
def medicine_delete(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)

    if request.method == "POST":
        medicine.delete()
        return redirect("managers:medicine-list")

    return render(request, "managers/medicine_confirm_delete.html", {
        "medicine": medicine
    })

@allow_manager
def category_list(request):
    categories = Category.objects.order_by("name")
    return render(request, "managers/category_list.html", {
        "categories": categories
    })

@allow_manager
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("managers:category-list")
    else:
        form = CategoryForm()
    return render(request, "managers/category_form.html", {"form": form})

@allow_manager
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("managers:category-list")
    else:
        form = CategoryForm(instance=category)
    return render(request, "managers/category_form.html", {
        "form": form, "is_edit": True
    })

@allow_manager
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect("managers:category-list")
    return render(request, "managers/category_confirm_delete.html", {
        "category": category
    })

@allow_manager
def order_list(request):
    orders = Order.objects.all().order_by("-created_at")
    return render(request, "managers/order_list.html", {
        "orders": orders
    })

@allow_manager
def update_order_status(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.method == "POST":
        new_status = request.POST.get("status")
        order.status = new_status
        order.save()

    return redirect("managers:order-list")