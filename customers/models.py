from django.db import models
from django.conf import settings
from managers.models import Medicine

class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses"
    )
    line1 = models.CharField(max_length=225)
    line2 = models.CharField(max_length=225, blank=True)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.line1}, {self.city} - {self.pincode}"
    
class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="carts",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.pk} for {self.user}"
    
    @property
    def total(self):
        return sum(item.line_total for item in self.items.all())
    
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete = models.CASCADE,
        related_name="items"
    )
    medicine = models.ForeignKey(
        Medicine,
        on_delete = models.CASCADE,
        related_name = "cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    class Meta:
        unique_together = ("cart", "medicine")

    def __str__(self):
        return f"{self.medicine.name} x {self.quantity}"

    @property
    def line_total(self):
        return self.medicine.price * self.quantity