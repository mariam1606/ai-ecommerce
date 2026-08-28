from django.urls import path

from .views import (
    checkout,
    order_detail,
    order_history,
)


urlpatterns = [
    path("checkout/", checkout, name="checkout"),
    path("history/", order_history, name="order_history"),
    path(
        "<int:order_id>/",
        order_detail,
        name="order_detail",
    ),
]