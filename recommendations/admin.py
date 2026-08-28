from django.contrib import admin

from .models import ProductInteraction


@admin.register(ProductInteraction)
class ProductInteractionAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "product",
        "interaction_type",
        "created_at",
    )

    list_filter = (
        "interaction_type",
        "created_at",
    )

    search_fields = (
        "user__username",
        "product__name",
    )