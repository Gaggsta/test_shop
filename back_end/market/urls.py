from django.urls import path
from . import views

urlpatterns = [
    path("cart/",
         views.CartAPI.as_view()),
    path("create_order/", views.CreateOrderAPI.as_view()),
    path("print_order/", views.Order_printAPI.as_view())

]
