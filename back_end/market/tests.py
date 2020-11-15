from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from .models import Products, Cart, Order
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class SigninTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@test.com', password='Testtest12', first_name='first_name',
            second_name='second_name', middle_name='middle_name', address='address',
            role="менеджер")
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(email='test@test.com', password='Testtest12')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='Testtest12')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(username='Testtest12', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)


class ProductsTest(TestCase):

    def setUp(self):
        self.product = Products.objects.create(
            vendor_code='PT1123', name='Testtest12', purchase_price=1, sale_price=2)

    def tearDown(self):
        self.product.delete()

    def test_correct(self):
        prod = Products.objects.get(
            vendor_code='PT1123', name='Testtest12')
        self.assertTrue((prod is not None) and (
            prod.purchase_price == 1) and (prod.sale_price == 2))


class OrderTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@test.com', password='Testtest12', first_name='first_name',
            second_name='second_name', middle_name='middle_name', address='address',
            role="менеджер")
        self.user.save()
        self.product = Products.objects.create(
            vendor_code='PT1123', name='Testtest12', purchase_price=1, sale_price=2)
        self.order = Order.objects.create(client=self.user)
        self.cart = Cart.objects.create(
            client=self.user, product=self.product, number=2, order=self.order)

    def tearDown(self):
        self.user.delete()
        self.product.delete()
        self.order.delete()
        self.cart.delete()

    def test_correct(self):
        order = Order.objects.get(id=self.order.id)
        self.assertTrue((order is not None) and (
            order.client == self.user) and (order.dest_address() == self.user.address) and (order.total() == 4))


class CartTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@test.com', password='Testtest12', first_name='first_name',
            second_name='second_name', middle_name='middle_name', address='address',
            role="менеджер")
        self.user.save()
        self.product = Products.objects.create(
            vendor_code='PT1123', name='Testtest12', purchase_price=1, sale_price=2)
        self.cart = Cart.objects.create(
            client=self.user, product=self.product, number=2)

    def tearDown(self):
        self.user.delete()
        self.product.delete()
        self.cart.delete()

    def test_correct(self):
        cart_prod = Cart.objects.get(client=self.user)
        self.assertTrue((
            cart_prod.product == self.product) and (cart_prod.number == 2)
            and (cart_prod.price() == 2) and (cart_prod.total() == 4))


class SigninAPITest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@test.com', password='Testtest12', first_name='first_name',
            second_name='second_name', middle_name='middle_name', address='address',
            role="менеджер")
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        response = self.client.post('http://127.0.0.1:8000/auth/token/login/', {
                                    'email': 'test@test.com', 'password': 'Testtest12'})
        self.assertTrue(response.status_code == 200)

    def test_wrong_username(self):
        response = self.client.post('http://127.0.0.1:8000/auth/token/login/', {
                                    'email': 'wrong@test.com', 'password': 'Testtest12'})
        self.assertTrue(response.status_code == 400)

    def test_wrong_pssword(self):
        response = self.client.post('http://127.0.0.1:8000/auth/token/login/', {
                                    'email': 'wrong@test.com', 'password': 'Testtest11'})
        self.assertTrue(response.status_code == 400)


class CartAPITest(APITestCase):

    def setUp(self):
        self.manager = get_user_model().objects.create_user(
            email='test@test.com', password='Testtest12', first_name='first_name',
            second_name='second_name', middle_name='middle_name', address='address',
            role="менеджер")
        self.manager.save()
        self.user = get_user_model().objects.create_user(
            email='user@test.com', password='Usertest12', first_name='first_user',
            second_name='second_user', middle_name='middle_user', address='address',
            role="клиент")
        self.user.save()
        self.product = Products.objects.create(
            vendor_code='PT1123', name='Testtest12', purchase_price=1, sale_price=2)
        self.cart = Cart.objects.create(
            client=self.user, product=self.product, number=2)
        self.user_token = self.client.post('http://127.0.0.1:8000/auth/token/login/', {
            'email': 'user@test.com', 'password': 'Usertest12'}).data['auth_token']
        self.manager_token = self.client.post('http://127.0.0.1:8000/auth/token/login/', {
            'email': 'test@test.com', 'password': 'Testtest12'}).data['auth_token']

    def tearDown(self):
        self.user.delete()
        self.manager.delete()
        self.product.delete()
        self.cart.delete()

    def test_cart_get(self):
        """
        User get his cart
        """
        response = self.client.get('http://127.0.0.1:8000/api/v1/cart/',
                                   {'user_id': self.user.id}, HTTP_AUTHORIZATION='Token ' + self.user_token)
        print(self.user.id)
        self.assertEqual(
            response.content, b'[{"client":2,"product":1,"number":2,"price":2.0,"total":4.0}]')

    def test_cart_get2(self):
        """
        User get managers cart
        """
        response = self.client.get('http://127.0.0.1:8000/api/v1/cart/',
                                   {'user_id': self.manager.id}, HTTP_AUTHORIZATION='Token ' + self.user_token)
        self.assertTrue(response.status_code == 403)

    def test_cart_get3(self):
        """
        Manager get users cart
        """
        response = self.client.get('http://127.0.0.1:8000/api/v1/cart/',
                                   {'user_id': self.user.id}, HTTP_AUTHORIZATION='Token ' + self.manager_token)
        self.assertEqual(
            response.content, b'[{"client":6,"product":3,"number":2,"price":2.0,"total":4.0}]')

    def test_cart_post(self):
        """
        Manager add to user cart
        """
        response = self.client.post('http://127.0.0.1:8000/api/v1/cart/',
                                    {'user_id': self.user.id, 'prod_id': self.product.id, 'number': 2}, HTTP_AUTHORIZATION='Token ' + self.manager_token)
        self.assertEqual(
            response.content, b'[{"client":8,"product":4,"number":4,"price":2.0,"total":8.0}]')

    def test_cart_post2(self):
        """
        User add to cart
        """
        response = self.client.post('http://127.0.0.1:8000/api/v1/cart/',
                                    {'user_id': self.user.id, 'prod_id': self.product.id, 'number': 2}, HTTP_AUTHORIZATION='Token ' + self.user_token)
        self.assertEqual(
            response.content, b'[{"client":10,"product":5,"number":4,"price":2.0,"total":8.0}]')
