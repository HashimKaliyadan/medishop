from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from managers.models import Category, Medicine
from .models import Cart, CartItem, Address, Order, OrderItem
from .serializers import (
    CategorySerializer, MedicineSerializer, CartSerializer, CartItemSerializer, AddressSerializer, OrderSerializer
)

@api_view(['GET'])
@permission_classes([AllowAny])
def categories_list(request):
    qs = Category.objects.filter(is_active=True).order_by('name')
    data = CategorySerializer(qs, many=True).data
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])
def category_medicines(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    qs = Medicine.objects.filter(category=category, in_stock=True).order_by('name')
    data = MedicineSerializer(qs, many=True, context={'request': request}).data
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])
def medicine_list(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()

    medicines = Medicine.objects.filter(in_stock=True)
    if query:
        medicines = medicines.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    if category_slug:
        medicines = medicines.filter(category__slug=category_slug)

    data = MedicineSerializer(medicines.order_by('name'), many=True, context={'request': request}).data
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])
def medicine_detail(request, slug):
    medicine = get_object_or_404(Medicine, slug=slug, in_stock=True)
    data = MedicineSerializer(medicine, context={'request': request}).data
    return Response(data)

# Cart APIs (requires auth)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    serializer = CartSerializer(cart, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    medicine_id = request.data.get('medicine_id')
    if not medicine_id:
        return Response({'error': 'medicine_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    medicine = get_object_or_404(Medicine, id=medicine_id, in_stock=True)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, medicine=medicine)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    serializer = CartSerializer(cart, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_cart_item(request):
    item_id = request.data.get('item_id')
    try:
        qty = int(request.data.get('quantity', 1))
    except (TypeError, ValueError):
        qty = 1
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if qty <= 0:
        item.delete()
    elif qty > 10:
        item.quantity = 10
        item.save()
    else:
        item.quantity = qty
        item.save()
    cart = item.cart
    serializer = CartSerializer(cart, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_cart_item(request):
    item_id = request.data.get('item_id')
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart = item.cart
    item.delete()
    serializer = CartSerializer(cart, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

    # stock check
    for item in cart.items.select_related('medicine'):
        if not item.medicine.in_stock:
            return Response({'error': 'Some items are out of stock'}, status=status.HTTP_400_BAD_REQUEST)

    prescription_required = any(item.medicine.is_prescription_required for item in cart.items.all())

    line1 = request.data.get('line1', '').strip()
    line2 = request.data.get('line2', '').strip()
    city = request.data.get('city', '').strip()
    pincode = request.data.get('pincode', '').strip()
    phone = request.data.get('phone', '').strip()
    prescription = request.FILES.get('prescription') if hasattr(request, 'FILES') else None

    if not line1 or not city or not pincode or not phone:
        return Response({'error': 'Address, City, Pincode, and Phone are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if prescription_required and not prescription:
        return Response({'error': 'Prescription required for one or more medicines.'}, status=status.HTTP_400_BAD_REQUEST)

    address = Address.objects.create(
        user=request.user,
        line1=line1,
        line2=line2,
        city=city,
        pincode=pincode,
        phone=phone
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

    cart.items.all().delete()
    serializer = OrderSerializer(order, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)
