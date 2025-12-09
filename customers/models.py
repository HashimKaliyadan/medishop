from django.db import models
from django.conf import settings
from managers.models import Medicine

class Address(models.Model):
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses"
    )
    line1=models.CharField(max_length=225)
    line2= models.CharField(max_length=225, blank=True)
    city=models.CharField(max_length=100)
    pincode=models.CharField(max_length=20)
    phone=models.CharField(max_length=15)
    is_default=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.line1}, {self.city} - {self.pincode}"
    
class Cart(models.Model):
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="carts",
        null=True,
        blank=True
    )
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.pk} for {self.user}"
    
    @property
    def total(self):
        return sum(item.line_total for item in self.items.all())
    
class CartItem(models.Model):
    cart=models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    medicine=models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    quantity=models.PositiveIntegerField(default=1)
    class Meta:
        unique_together=("cart", "medicine")

    def __str__(self):
        return f"{self.medicine.name} x {self.quantity}"

    @property
    def line_total(self):
        return self.medicine.price * self.quantity
    
ORDER_STATUS_CHOICES = [
    ("PENDING", "Pending"),
    ("PACKED", "Packed"),
    ("SHIPPED", "Shipped"),
    ("DELIVERED", "Delivered"),
]
    
class Order(models.Model):
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    address=models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="orders"
    )
    total=models.DecimalField(max_digits=10, decimal_places=2)
    status=models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default="PENDING"
    )
    prescription = models.FileField(upload_to='prescription/', blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.user} - {self.status}"
    
class OrderItem(models.Model):
    order=models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    medicine=models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name="order_items"
    )
    quantity=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.medicine.name} x {self.quantity}"

    @property
    def line_total(self):
        return self.price * self.quantity