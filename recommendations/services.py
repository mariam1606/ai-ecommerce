from collections import Counter

from django.db.models import Count

from products.models import Product
from .models import ProductInteraction


def get_trending_products(limit=6):
    products = Product.objects.filter(
        stock__gt=0
    ).annotate(
        interaction_count=Count("interactions")
    ).order_by(
        "-interaction_count",
        "-created_at"
    )[:limit]

    return [
        {
            "product": product,
            "reason": "This product is currently popular with customers.",
            "score": product.interaction_count,
        }
        for product in products
    ]


def get_personalized_recommendations(user, limit=6):
    interactions = ProductInteraction.objects.filter(
        user=user
    ).select_related(
        "product",
        "product__category"
    )

    if not interactions.exists():
        return get_trending_products(limit)

    categories = Counter(
        interaction.product.category_id
        for interaction in interactions
        if interaction.product.category_id
    )

    recommendations = []

    for category_id, count in categories.most_common():

        products = Product.objects.filter(
            category_id=category_id,
            stock__gt=0
        ).exclude(
            interactions__user=user
        ).annotate(
            interaction_count=Count("interactions")
        ).order_by(
            "-interaction_count",
            "-created_at"
        )

        for product in products:

            recommendations.append({
                "product": product,
                "reason": (
                    f"Recommended because you interact frequently "
                    f"with {product.category.name} products."
                ),
                "score": count,
            })

            if len(recommendations) >= limit:
                return recommendations

    if len(recommendations) < limit:
        recommendations.extend(
            get_trending_products(
                limit - len(recommendations)
            )
        )

    return recommendations[:limit]


def get_recommendations(user, limit=6):
    return get_personalized_recommendations(user, limit)


def get_similar_products(product, limit=6):
    products = Product.objects.filter(
        category=product.category,
        stock__gt=0
    ).exclude(
        id=product.id
    ).annotate(
        interaction_count=Count("interactions")
    ).order_by(
        "-interaction_count",
        "-created_at"
    )[:limit]

    return [
        {
            "product": item,
            "reason": (
                f"Similar to {product.name} because it belongs "
                f"to the same category."
            ),
            "score": item.interaction_count,
        }
        for item in products
    ]


def explain_recommendation(product, reason=None):
    if reason:
        return reason

    return (
        f"We recommend {product.name} because it matches "
        f"your interests and shopping activity."
    )