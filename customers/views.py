from django.shortcuts import render, get_object_or_404, redirect
from managers.models import Category, Medicine
from .models import Cart, CartItem, Order, OrderItem, Address
from django.contrib.auth.decorators import login_required
from django.db.models import Q

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
    # get query params
    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()

    # base queryset (only available medicines)
    medicines = Medicine.objects.filter(in_stock=True)

    # search by name or description
    if query:
        medicines = medicines.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # filter by category
    if category_slug:
        medicines = medicines.filter(category__slug=category_slug)

    # active categories for filter dropdown
    categories = Category.objects.filter(is_active=True)

    context = {
        "medicines": medicines.order_by("name"),
        "categories": categories,
        "query": query,
        "selected_category": category_slug,
    }

    return render(request, "customers/all_medicines.html", context)

def medicine_detail(request, slug):
    medicine = get_object_or_404(Medicine, slug=slug, in_stock=True)
    return render(request, "customers/medicine_detail.html", {
        "medicine": medicine
    })

@login_required
def add_to_cart(request, medicine_id):
    medicine = get_object_or_404(
        Medicine,
        id=medicine_id,
        in_stock=True   # 🔒 hard check
    )

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

    # remove broken cart items
    cart.items.filter(medicine__isnull=True).delete()

    return render(request, "customers/cart.html", {"cart": cart})

@login_required
def update_cart(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if request.method == "POST":
        try:
            qty = int(request.POST.get("quantity", 1))
        except ValueError:
            qty = 1

        if qty <= 0:
            item.delete()
        elif qty > 10:              # 🔒 limit
            item.quantity = 10
            item.save()
        else:
            item.quantity = qty
            item.save()

    return redirect("customers:cart")


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect("customers:cart")

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()

    # cart must exist and have items
    if not cart or not cart.items.exists():
        return redirect("customers:cart")

    # 🔒 FINAL STOCK CHECK (very important)
    for item in cart.items.select_related("medicine"):
        if not item.medicine.in_stock:
            return redirect("customers:cart")

    # check if any medicine requires prescription
    prescription_required = any(
        item.medicine.is_prescription_required
        for item in cart.items.all()
    )

    if request.method == "POST":
        address_text = request.POST.get("address", "").strip()
        pincode = request.POST.get("pincode", "").strip()
        prescription = request.FILES.get("prescription")

        # basic validation
        if not address_text or not pincode:
            return render(request, "customers/checkout.html", {
                "cart": cart,
                "prescription_required": prescription_required,
                "error": "Address and pincode are required.",
            })

        if prescription_required and not prescription:
            return render(request, "customers/checkout.html", {
                "cart": cart,
                "prescription_required": prescription_required,
                "error": "Prescription is required for one or more medicines.",
            })

        # create address
        address = Address.objects.create(
            user=request.user,
            address=address_text,
            pincode=pincode
        )

        # create order
        order = Order.objects.create(
            user=request.user,
            address=address,
            total=cart.total,
            prescription=prescription
        )

        # create order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                medicine=item.medicine,
                quantity=item.quantity,
                price=item.medicine.price
            )

        # clear cart
        cart.items.all().delete()

        return redirect("customers:order-success", order_id=order.id)

    return render(request, "customers/checkout.html", {
        "cart": cart,
        "prescription_required": prescription_required,
    })

@login_required
def order_success(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, "customers/order_success.html", {"order": order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "customers/order_list.html", {
        "orders": orders
    })