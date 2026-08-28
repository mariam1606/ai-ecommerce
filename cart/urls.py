from django.urls import path

from .views import (
    add_to_cart,
    cart_detail,
    remove_from_cart,
    update_cart,
)


urlpatterns = [
    path("", cart_detail, name="cart_detail"),
    path("add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("update/<int:item_id>/", update_cart, name="update_cart"),
    path("remove/<int:item_id>/", remove_from_cart, name="remove_from_cart"),
]