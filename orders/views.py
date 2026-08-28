from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from cart.models import Cart

from .models import Order, OrderItem


@login_required
@transaction.atomic
def checkout(request):

    cart = get_object_or_404(
        Cart,
        user=request.user,
    )

    items = list(
        cart.items.select_related("product")
    )

    if not items:
        messages.error(request, "Your cart is empty.")
        return redirect("cart_detail")

    for item in items:
        if item.quantity > item.product.stock:
            messages.error(
                request,
                f"Not enough stock for {item.product.name}.",
            )
            return redirect("cart_detail")

    order = Order.objects.create(
        user=request.user,
        total_price=0,
    )

    total = 0

    for item in items:

        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )

        total += item.product.price * item.quantity

        item.product.stock -= item.quantity
        item.product.save(update_fields=["stock"])

    order.total_price = total
    order.save(update_fields=["total_price"])

    cart.items.all().delete()

    messages.success(
        request,
        f"Order #{order.id} placed successfully.",
    )

    return redirect("order_detail", order_id=order.id)


@login_required
def order_history(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "orders/order_history.html",
        {"orders": orders},
    )


@login_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    return render(
        request,
        "orders/order_detail.html",
        {"order": order},
    )