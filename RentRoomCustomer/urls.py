from django.urls import path
from RentRoomCustomer import views

urlpatterns = [
    path("", views.home, name="login"),
]