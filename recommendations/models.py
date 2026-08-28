from django.conf import settings
from django.db import models

from products.models import Product


class ProductInteraction(models.Model):

    INTERACTION_CHOICES = [
        ("view", "View"),
        ("cart", "Cart"),
        ("purchase", "Purchase"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="product_interactions",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="interactions",
    )

    interaction_type = models.CharField(
        max_length=20,
        choices=INTERACTION_CHOICES,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.product.name} - "
            f"{self.interaction_type}"
        )