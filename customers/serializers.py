from rest_framework import serializers
from managers.models import Category, Medicine
from .models import Cart, CartItem, Address, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class MedicineSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Medicine
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'in_stock',
            'is_prescription_required', 'category', 'image'
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            try:
                url = obj.image.url
            except Exception:
                return None
            if request:
                return request.build_absolute_uri(url)
            return url
        return None

class CartItemSerializer(serializers.ModelSerializer):
    medicine = MedicineSerializer(read_only=True, context={'request': None})
    line_total = serializers.DecimalField(source='line_total', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'medicine', 'quantity', 'line_total']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(source='total', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'line1', 'line2', 'city', 'pincode', 'phone', 'is_default']

class OrderItemSerializer(serializers.ModelSerializer):
    medicine = MedicineSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'medicine', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'address', 'total', 'status', 'prescription', 'created_at', 'items']
