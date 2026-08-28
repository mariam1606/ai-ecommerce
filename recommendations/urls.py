from django.urls import path

from .views import recommendations_view


urlpatterns = [
    path(
        "",
        recommendations_view,
        name="recommendations",
    ),
]