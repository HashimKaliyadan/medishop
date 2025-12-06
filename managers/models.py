from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    class Medicine(models.Model):
        category = models.ForeignKey(
            Category,
            on_delete=models.CASCADE,
            related_name='medicines',
        )