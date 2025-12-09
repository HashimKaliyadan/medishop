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
    