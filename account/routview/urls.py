from django.urls import path, include
from .views import Register

urlpatterns = [
    path('register/', Register.as_view()),
]
