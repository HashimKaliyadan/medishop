from django.shortcuts import render, get_object_or_404, redirect
from managers.models import Category, Medicine
from .models import Cart, CartItem, Order, OrderItem, Address
from django.contrib.auth.decorators import login_required

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

@login_required
def add_to_cart(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id, in_stock=True)

    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        medicine=medicine
    )

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect("customers:cart")

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, "customers/cart.html", {"cart": cart})

@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == "POST":
        qty = int(request.POST.get("quantity", 1))
        if qty > 0:
            item.quantity = qty
            item.save()
        else:
            item.delete()

    return redirect("customers:cart")

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect("customers:cart")

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not cart.items.exists():
        return redirect("customers:cart")

    # check if prescription is required
    prescription_required = any(
        item.medicine.is_prescription_required
        for item in cart.items.all()
    )

    if request.method == "POST":
        address_text = request.POST.get("address")
        pincode = request.POST.get("pincode")
        prescription = request.FILES.get("prescription")

        if prescription_required and not prescription:
            return render(request, "customers/checkout.html", {
                "cart": cart,
                "error": "Prescription required for one or more medicines.",
                "prescription_required": prescription_required,
            })

        address = Address.objects.create(
            user=request.user,
            address=address_text,
            pincode=pincode
        )

        order = Order.objects.create(
            user=request.user,
            address=address,
            total=cart.total,
            prescription=prescription
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                medicine=item.medicine,
                quantity=item.quantity,
                price=item.medicine.price
            )

        cart.items.all().delete()  # clear cart

        return redirect("customers:order-success", order_id=order.id)

    return render(request, "customers/checkout.html", {
        "cart": cart,
        "prescription_required": prescription_required,
    })

@login_required
def order_success(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, "customers/order_success.html", {"order": order})

