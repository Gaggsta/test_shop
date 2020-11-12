from typing import Type
from rest_framework import permissions
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, HttpResponseServerError
import logging
from .models import Cart, Order, Products
from .serializers import CertSerializer
from .tasks import save_to_pdf

logger = logging.getLogger(__name__)


class CartAPI(APIView):
    """
    interface for working with cart

    GET: show cart by user_id
    req.:
        cart owner id

    POST: add productid to the cart of user_id
    req.:
        cart owner id
        product id
        number of product


    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        requester = User.objects.get(username=request.user)
        try:
            user = User.objects.get(id=int(request.GET.get('user_id')))
        except:
            logger.warning(
                f"{requester.id} {request.GET.get('user_id')} wrong format user_id")
            return HttpResponseBadRequest()
        if requester.id == user.id or requester.profile.role == 'менеджер':
            cart = Cart.objects.filter(
                client=user.profile).exclude(order__isnull=True)
            queryset = CertSerializer(instance=cart, many=True,)
            return Response(queryset.data)
        else:
            logger.warning(
                f"{requester.id} {request.GET.get('user_id')} permission_denied")
            raise PermissionDenied()

    def post(self, request, *args, **kwargs):
        requester = User.objects.get(username=request.user)
        try:
            user = User.objects.get(id=int(request.GET.get('user_id')))
        except:
            logger.warning(
                f"{requester.id} {request.GET.get('user_id')} wrong format user_id")
            return HttpResponseBadRequest()
        if requester.id == user.id or requester.profile.role == 'менеджер':
            try:
                prod_id = int(request.GET.get('prod_id'))
                prod = Products.objects.get(id=prod_id)
            except:
                logger.warning(
                    f"{requester.id} {request.GET.get('user_id')} wrong format prod_id")
                return HttpResponseBadRequest()
            try:
                number = int(request.GET.get('number'))
                if number < 1:
                    raise TypeError
            except:
                logger.warning(
                    f"{requester.id} {request.GET.get('user_id')} wrong format number")
                return HttpResponseBadRequest()
            try:
                cart = Cart.objects.get(client=user.profile, product=prod)
                print(cart.number)
                cart.number = cart.number + number
                cart.save()
            except:
                cart = Cart.objects.create(
                    client=user.profile, product=prod, number=number)
            cart = Cart.objects.filter(client=user.profile)
            queryset = CertSerializer(instance=[cart], many=True,)
            return Response(queryset.data)
        else:
            logger.warning(
                f"{requester.id} {request.GET.get('user_id')} permission_denied")
            raise PermissionDenied()


class Order_printAPI(APIView):
    """take order number  and make task for printing it

    req:
        order_id
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        requester = User.objects.get(username=request.user)
        if requester.profile.role == 'менеджер':
            try:
                order = Order.objects.get(id=int(request.GET.get('order_id')))
            except:
                logger.warning(
                    f"{requester.id} {request.GET.get('user_id')} wrong format order_id")
                return HttpResponseBadRequest()
            html_content = f"<!DOCTYPE html><html><head><meta charset='utf-8'></head><body><p>Клиент: {order.client()}</p><p>Номер заказа: {order.id}</p><p>Адрес доставки: {order.dest_address()}</p><body></html>"
            if save_to_pdf.delay(html_content, order.id):
                res = {"code": 200, "message": "Файл сохранен"}
                return Response(data=res, status=200)
            else:
                return HttpResponseServerError()
