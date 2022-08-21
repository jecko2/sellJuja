from django.urls import path, include
from .views import Register, LoginView, UserView, LogoutView

urlpatterns = [

    path('register/', Register.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),

    path('user/', UserView.as_view())
]
