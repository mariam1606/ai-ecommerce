from recommendations.models import ProductInteraction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product

from .models import Cart, CartItem


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    return render(
        request,
        "cart/cart_detail.html",
        {
            "cart": cart,
            "items": cart.items.select_related("product"),
        },
    )


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect("product_detail", product_id=product.id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
    )

    if not created:
        if item.quantity < product.stock:
            item.quantity += 1
            item.save()
        else:
            messages.error(request, "Not enough stock available.")
            return redirect("cart_detail")

    ProductInteraction.objects.create(
        user=request.user,
        product=product,
        interaction_type="cart",
    )

    messages.success(request, "Product added to cart.")

    return redirect("cart_detail")


@login_required
def update_cart(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user,
    )

    if request.method == "POST":
        try:
            quantity = int(request.POST.get("quantity", 1))
        except (TypeError, ValueError):
            quantity = 1

        if quantity <= 0:
            item.delete()

        elif quantity <= item.product.stock:
            item.quantity = quantity
            item.save()

        else:
            messages.error(request, "Requested quantity is not available.")

    return redirect("cart_detail")


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user,
    )

    item.delete()

    messages.success(request, "Product removed from cart.")

    return redirect("cart_detail")