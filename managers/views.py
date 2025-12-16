from django.shortcuts import render , redirect , get_object_or_404
from main.decorators import allow_manager
from managers.models import Category, Medicine
from customers.models import Order
from .forms import MedicineForm, CategoryForm


@allow_manager
def dashboard(request):
    context = {
        "total_categories": Category.objects.count(),
        "total_medicines": Medicine.objects.count(),
        "total_orders": Order.objects.count(),
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