from typing import Type
from rest_framework import permissions
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, HttpResponseServerError
import logging
from .models import Cart, Order, Products
from .serializers import CertSerializer, OrderSerializer
from .tasks import save_to_pdf

logger = logging.getLogger(__name__)


class CartAPI(APIView):
    """
    interface for working with cart

    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        GET: show cart by user_id
        req.:
            cart owner id
        """
        requester = get_user_model().objects.get(email=request.user)
        try:
            user = get_user_model().objects.get(id=int(request.GET.get('user_id')))
        except:
            logger.warning(
                f"{requester.id} {request.GET.get('user_id')} wrong format user_id")
            return HttpResponseBadRequest('wrong format user_id')
        if requester.id == user.id or requester.role == "менеджер":
            cart = Cart.objects.filter(
                client=user).exclude(order__isnull=False)
            queryset = CertSerializer(instance=cart, many=True,)
            return Response(queryset.data)
        else:
            logger.warning(
                f"{requester.id} {request.GET.get('user_id')} permission_denied")
            raise PermissionDenied()

    def post(self, request, *args, **kwargs):
        """
        POST: add productid to the cart of user_id
        req.:
            cart owner id
            product id
            number of product
        """
        # я не знаю почему,
        # но у меня постман отправлял POST запросы,
        # а все данные были в request.GET

        if request.GET:
            qd = request.GET
        else:
            qd = request.POST
        requester = get_user_model().objects.get(email=request.user)
        try:
            user = get_user_model().objects.get(id=int(qd.get('user_id')))
        except:
            logger.warning(
                f"{requester.id} {qd.get('user_id')} wrong format user_id")
            return HttpResponseBadRequest('wrong format user_id')
        if requester.id == user.id or requester.role == "менеджер":
            try:
                prod_id = int(qd.get('prod_id'))
                prod = Products.objects.get(id=prod_id)
            except:
                logger.warning(
                    f"{requester.id} {qd.get('user_id')} wrong format prod_id")
                return HttpResponseBadRequest('wrong format prod_id')
            try:
                number = int(qd.get('number'))
                if number < 1:
                    raise TypeError
            except:
                logger.warning(
                    f"{requester.id} {qd.get('user_id')} wrong format number")
                return HttpResponseBadRequest('wrong format number')
            try:
                cart = Cart.objects.get(client=user, product=prod)
                cart.number = cart.number + number
                cart.save()
            except:
                cart = Cart.objects.create(
                    client=user, product=prod, number=number)
            cart = Cart.objects.filter(
                client=user).exclude(order__isnull=False)
            queryset = CertSerializer(instance=cart, many=True,)
            return Response(queryset.data)
        else:
            logger.warning(
                f"{requester.id} {qd.get('user_id')} permission_denied")
            raise PermissionDenied()


class CreateOrderAPI(APIView):
    """
    Make order by user_id from they cart
    req:
        user_id
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.GET:
            qd = request.GET
        else:
            qd = request.POST
        requester = get_user_model().objects.get(email=request.user)
        try:
            user = get_user_model().objects.get(id=int(qd.get('user_id')))
        except:
            logger.warning(
                f"{requester.id} {qd.get('user_id')} wrong format user_id")
            return HttpResponseBadRequest('wrong format user_id')
        if Cart.objects.filter(client=user).exclude(order__isnull=False):
            if requester.role == "менеджер":
                order = Order.objects.create(client=user)
                queryset = OrderSerializer(instance=order, many=False,)
                return Response(queryset.data)
            else:
                logger.warning(
                    f"{requester.id} {qd.get('user_id')} permission_denied")
                raise PermissionDenied()
        else:
            logger.warning(
                f"{requester.id} {qd.get('user_id')} cart is empty")
            return HttpResponseBadRequest('cart is empty')


class Order_printAPI(APIView):
    """take order number  and make task for printing it

    req:
        order_id
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # я не знаю почему,
        # но у меня постман отправлял POST запросы,
        # а все данные были в request.GET
        if request.GET:
            qd = request.GET
        else:
            qd = request.POST
        requester = get_user_model().objects.get(email=request.user)
        if requester.role == "менеджер":
            try:
                print(requester)
                order = Order.objects.get(
                    id=int(qd.get('order_id')))
            except:
                logger.warning(
                    f"{requester.id} {qd.get('order_id')} wrong format order_id")
                return HttpResponseBadRequest('wrong format order_id')
            html_content = f"<!DOCTYPE html><html><head><meta charset='utf-8'></head><body><p>Клиент: {order.client}</p><p>Номер заказа: {order.id}</p><p>Адрес доставки: {order.dest_address()}</p><body></html>"
            if save_to_pdf.delay(html_content, order.id):
                res = {"code": 200, "message": "Файл сохранен"}
                return Response(data=res, status=200)
            else:
                logger.warning(
                    f"{requester.id} {qd.get('order_id')} something going wrong")
                return HttpResponseServerError('something going wrong')
        else:
            logger.warning(
                f"{requester.id} {qd.get('order_id')} permission_denied")
            raise PermissionDenied()
