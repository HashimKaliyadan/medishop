from django.urls import path
from . import api_views

urlpatterns = [
    path('categories/', api_views.categories_list, name='api-categories'),
    path('categories/<slug:slug>/medicines/', api_views.category_medicines, name='api-category-medicines'),

    path('medicines/', api_views.medicine_list, name='api-medicine-list'),
    path('medicines/<slug:slug>/', api_views.medicine_detail, name='api-medicine-detail'),

    # cart
    path('cart/', api_views.cart_view, name='api-cart'),
    path('cart/add/', api_views.add_to_cart, name='api-cart-add'),
    path('cart/update/', api_views.update_cart_item, name='api-cart-update'),
    path('cart/remove/', api_views.remove_cart_item, name='api-cart-remove'),
    path('checkout/', api_views.checkout, name='api-checkout'),
]
