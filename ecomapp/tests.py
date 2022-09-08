"""
     this test case file is for the different form for the user
 """
from django.test import TestCase
from .models import User, Product


# Create your tests here.

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='ritik1', first_name="Ritik", email='ritik@gmail.com',
                            user_type='customer', mobile_no='987654329', addressof_customer='vill.kamed ratlam',
                            gender='Male', password='deq12345')
        User.objects.create(username='abhishek', first_name="Abhishek", email='abhishek@gmail.com',
                            user_type='customer', mobile_no='987654999', addressof_customer='vill.kamed ratlam',
                            gender='Male', password='deq12345')

    def test_user_test(self):
        obj = User.objects.get(username='ritik1')
        # print(obj)
        obj1 = User.objects.get(username='abhishek')
        # print(obj1)
        self.assertEqual(obj.username, 'ritik1')
        self.assertEqual(obj1.username, 'abhishek')


class ProductTestCase(TestCase):
    def setUp(self):
        user = User(username='ritik1', first_name="Ritik", email='ritik@gmail.com',
                    user_type='customer', mobile_no='987654329', addressof_customer='vill.kamed ratlam',
                    gender='Male', password='deq12345')
        user.save()
        Product.objects.create(product_type='Track-pents', product_name="Adidas",
                               description='new slim fit trak pents for the 20 years', price='2000',
                               product_img='', user=user,
                               gender='Male', quantity='4')

    def test_product_test(self):
        obj = Product.objects.get(product_type='Track-pents')
        print(obj)
        print(obj.user)
        self.assertEqual(obj.product_type, 'Track-pents')
        # self.assertEqual(obj1.username, 'abhi')


class VariationsTestCase(TestCase):
    def setUp(self):
        user = User(username='ritik1', first_name="Ritik", email='ritik@gmail.com',
                    user_type='customer', mobile_no='987654329', addressof_customer='vill.kamed ratlam',
                    gender='Male', password='deq12345')
        user.save()
        Product.objects.create(product_type='Track-pents', product_name="Adidas",
                               description='new slim fit trak pents for the 20 years', price='2000',
                               product_img='', user=user,
                               gender='Male', quantity='4')

    def test_product_test(self):
        obj = Product.objects.get(product_type='Track-pents')
        print(obj)
        print(obj.user)
        self.assertEqual(obj.product_type, 'Track-pents')
