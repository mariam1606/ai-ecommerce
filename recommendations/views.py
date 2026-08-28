from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .services import (
    explain_recommendation,
    get_recommendations,
)


@login_required
def recommendations_view(request):

    products = get_recommendations(
        request.user,
        limit=6,
    )

    recommendations = [
        {
            "product": product,
            "explanation": explain_recommendation(product),
        }
        for product in products
    ]

    return render(
        request,
        "recommendations/recommendations.html",
        {
            "recommendations": recommendations,
        },
    )