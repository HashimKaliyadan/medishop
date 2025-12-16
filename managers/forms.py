from django import forms
from .models import Medicine , Category

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = [
            "category",
            "name",
            "slug",
            "description",
            "price",
            "in_stock",
            "is_prescription_required",
            "image",
        ]
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug", "description", "is_active"]