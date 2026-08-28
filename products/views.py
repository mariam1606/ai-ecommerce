from recommendations.models import ProductInteraction
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def home(request):
    products = Product.objects.all().order_by("-created_at")[:8]
    categories = Category.objects.all()

    return render(
        request,
        "home.html",
        {
            "products": products,
            "categories": categories,
        },
    )


def product_list(request):
    products = Product.objects.all().order_by("-created_at")
    categories = Category.objects.all()

    search_query = request.GET.get("search", "").strip()
    category_id = request.GET.get("category", "").strip()

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "categories": categories,
            "search_query": search_query,
            "selected_category": category_id,
        },
    )


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        ProductInteraction.objects.create(
            user=request.user,
            product=product,
            interaction_type="view",
        )

    similar_products = (
        Product.objects.filter(category=product.category)
        .exclude(id=product.id)
        .order_by("-created_at")[:4]
    )

    return render(
        request,
        "products/product_detail.html",
        {
            "product": product,
            "similar_products": similar_products,
        },
    )