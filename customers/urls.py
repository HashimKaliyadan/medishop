from django.urls import path
from . import views

app_name = "customers"

urlpatterns = [
    path("", views.customer_home, name="home"),
    path("categories/", views.category_list, name="category-list"),
    path("categories/<slug:slug>/", views.medicine_list_by_category, name="medicine-by-category"),
    path("medicines/", views.all_medicines, name="medicine-list"),
    path("medicine/<slug:slug>/", views.medicine_detail, name="medicine-detail"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:medicine_id>/", views.add_to_cart, name="add-to-cart"),
    path("cart/update/<int:item_id>/", views.update_cart, name="update-cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove-from-cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/success/<int:order_id>/", views.order_success, name="order-success"),
    path("orders/", views.order_list, name="order-list"),
]
