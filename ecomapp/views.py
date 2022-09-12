"""
   this contains all the functions in it
   """
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, DeleteView
from .models import User, Product, Wishlist, WishItems, CartItems, MyOrders
from .form import UpdateForm, CreatShopUser, Addproduct, ShopSignupForm, FinalAddress

TOTAL = 0


# Create your views here.
@login_required
def test(request):
    """
       this contains all the users in it whenever
       someone logins
    """
    current_user = request.user
    user = User.objects.get(username=current_user)
    products = Product.objects.all()
    # variations = Variations.objects.all()
    # print(user.__dict__)
    # import pdb;
    # pdb.set_trace()
    if user.user_type == 'admin':
        print("called!")
        return render(request, 'ecomapp/admin.html', {'t': current_user})
    elif user.user_type == 'shopuser':
        total_shell_product = current_user.product_set.all().aggregate(Sum('quantity'))
        total_recieved = MyOrders.objects.filter(user_id=current_user.id).aggregate(Sum('quantity'))
        total_sell = (total_recieved['quantity__sum'] / total_shell_product['quantity__sum']) * 100
        print(total_sell)
        return render(request, 'ecomapp/shopuser.html',
                      {'t': current_user, 'total_product_sell': total_sell})
    else:
        return render(request, 'ecomapp/customer.html', {'t': current_user, 'products': products})


class Test(ListView):
    """
         this contains all the users in it whenever
         someone logins
      """
    model = User

    def get_template_names(self):
        if self.request.user.user_type == 'admin':
            return ['ecomapp/admin.html']
        elif self.request.user.user_type == 'customer':
            return ['ecomapp/customer.html']
        else:
            return ['ecomapp/shopuser.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.user_type == 'customer':
            context['products'] = Product.objects.all()
        elif self.request.user.user_type == 'shopuser':
            # breakpoint()
            try:
                total_sell_product = self.request.user.product_set.all().aggregate(Sum('quantity'))
                total_recieved = MyOrders.objects.filter(user_id=self.request.user.id) \
                    .aggregate(Sum('quantity'))
                total_sell = (total_recieved['quantity__sum'] / total_sell_product['quantity__sum']) * 100
            except TypeError:
                total_sell = 0
            context['total_product_sell'] = total_sell
        return context


# def newshop_user(request):
#     """
#         this contains new shop user in django
#         we can add data
#      """
#     form = ShopSignupForm(request.POST or None)
#     if form.is_valid():
#         form.save(request)
#         return render(request, 'account/account_inactive.html')
#     context = {'form': form}
#     return render(request, 'account/shop_user.html', context)


class NewShopUser(View):
    """
        this contains new shop user in django
        we can add data
    """

    def get(self, request):
        form = ShopSignupForm()
        context = {'form': form}
        return render(request, 'account/shop_user.html', context)

    def post(self, request):
        form = ShopSignupForm(request.POST or None)
        if form.is_valid():
            print("sucess")
            form.save(request)
            return render(request, 'account/account_inactive.html')


# def update_order(request, pk):
#     """
#         this contains update order
#         data
#     """
#     obj = get_object_or_404(User, id=pk)
#     print(obj)
#     form = UpdateForm(request.POST or None, instance=obj)
#     context = {'form': form}
#     print(context)
#     if request.method == 'GET':
#         return render(request, 'ecomapp/update.html', context)
#     elif request.method == "POST":
#         # print("hereeeee post", data)
#         # User.objects.filter(id=request.POST)
#         if form.is_valid():
#             print("sucess")
#             form.save()
#             # return HttpResponse('success')
#         return render(request, 'ecomapp/update.html', context)
#         form = UpdateForm(instance=order)
#     print(form)
#     if request.method == 'POST':
#         print("post")
#         form = UpdateForm(request.POST, order)
#
#     print("get")
#     return render(request, 'ecomapp/update.html', context)

class UpdateOrder(View):
    """
        this contains update order
        data
    """

    def get(self, request, pk):
        obj = get_object_or_404(User, id=pk)
        print(obj)
        form = UpdateForm(instance=obj)
        context = {'form': form}
        return render(request, 'ecomapp/update.html', context)

    def post(self, request, pk):
        obj = get_object_or_404(User, id=pk)
        print(obj)
        form = UpdateForm(request.POST or None, instance=obj)
        if form.is_valid():
            print("sucess")
            form.save()
        return HttpResponse('success')


# def shop_user(request):
#     """
#         this contains function shop users
#     """
#     form = ShopUser(request.POST or None)
#     if form.is_valid():
#         form.save(request)
#     context = {'form': form}
#
#     return render(request, 'ecomapp/shopregis.html', context)


def shopuser_app(request, pk):
    """
        this contains function shop users app
    """
    print(pk)
    shopuser = User.objects.get(id=pk)
    print(shopuser)
    if request.method == 'POST' and 'approve' in request.POST:
        print("approve")
        shopuser.is_active = True
        shopuser.save()
        print(shopuser)
    elif request.method == 'POST' and 'reject' in request.POST:
        print("reject")
        shopuser.is_active = False
        shopuser.save()
        print(shopuser)
    context = {'username': shopuser.username, 'email': shopuser.email, 'name': shopuser.first_name}
    return render(request, 'ecomapp/userrequest.html', context)


class ShopUserRequest(TemplateView):
    """
        this contains function shop users app
    """
    template_name = 'ecomapp/userrequest.html'

    def post(self, request, **kwargs):
        shopuser = User.objects.get(id=kwargs['pk'])
        if 'approve' in request.POST:
            print("approve")
            shopuser.is_active = True
            shopuser.save()
        elif 'reject' in request.POST:
            print('reject')
            shopuser.is_active = False
            shopuser.save()
        return HttpResponse('success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(kwargs)
        context['shopuser'] = User.objects.get(id=kwargs['pk'])
        print(context['shopuser'].email)
        return context


def request_list(request):
    """
        this contains function request llist for users
    """
    print("requestlist")
    users_list = User.objects.filter(is_active=False)

    return render(request, 'ecomapp/adminrequest.html', {'context': users_list})


class RequestList(ListView):
    """
        this contains function request llist for users
    """
    # specify the model for list view
    model = User
    template_name = 'ecomapp/adminrequest.html'

    def get_queryset(self, *args, **kwargs):
        # context = super(ListProduct, self).get_queryset(*args, **kwargs)
        return User.objects.filter(is_active=False)


@login_required
def shop_list(request):
    """
         this contains function shop list for users
     """
    current_user = request.user
    if current_user.user_type == 'admin':
        shop_user_list = User.objects.filter(is_active=True, user_type='shopuser')
        return render(request, 'ecomapp/shopuserlist.html', {'shop_user_list': shop_user_list})
    return HttpResponse("Login Required")


class ShopList(ListView):
    """
         this contains function shop list for users
     """
    model = User
    template_name = 'ecomapp/shopuserlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.user_type == 'admin':
            context['shop_user_list'] = User.objects.filter(is_active=True, user_type='shopuser')
            context = {'shop_user_list': context['shop_user_list']}
            # print(context)
            return context
        return HttpResponse('Login Required')


def create_shopuser(request):
    """
        this contains function create shop user
    """
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreatShopUser(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            username = form.cleaned_data['username']
            gender = form.cleaned_data['gender']
            # user_type = form.cleaned_data['shopuser']
            shop_user_create = User(email=email, first_name=first_name, username=username,
                                    gender=gender, user_type='shopuser')
            shop_user_create.save()
            return HttpResponse('Saved')
        # if a GET (or any other method) we'll create a blank form
    else:
        form = CreatShopUser()
    return render(request, 'ecomapp/createshopuser.html', {'form': form})


class CreateShopUser(CreateView):
    """
        this contains function create shop user
    """
    # specify the model for create view
    model = User
    form_class = CreatShopUser
    template_name = 'ecomapp/createshopuser.html'

    def get_success_url(self):
        return reverse('ecomapp:ecomdash')


def add_product(request):
    """
        this contains function add products
    """
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Addproduct(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            addproduct_obj = form.save(commit=False)
            addproduct_obj.user = request.user
            addproduct_obj.save()
            return HttpResponse('Saved')
    else:
        form = Addproduct()
    return render(request, 'ecomapp/addproduct.html', {'form': form})


class AddProduct(View):
    """
        this contains function add products
    """

    def get(self, request):
        form = Addproduct()
        context = {'form': form}
        return render(request, 'ecomapp/addproduct.html', context)

    def post(self, request):
        form = Addproduct(request.POST or None, request.FILES)
        if form.is_valid():
            addproduct_obj = form.save(commit=False)
            print(addproduct_obj)
            addproduct_obj.user = request.user
            addproduct_obj.save()
            print("sucess")
        return HttpResponse('success')


@login_required
def list_product(request):
    """
        this contains function list of product
    """
    current_user = request.user
    user_product = current_user.product_set.all()
    return render(request, 'ecomapp/product_list.html', {'user_product': user_product})


class ListProduct(ListView):
    """
        this contains function list of product
    """
    # specify the model for list view
    model = Product
    template_name = 'ecomapp/product_list.html'

    def get_queryset(self, *args, **kwargs):
        # context = super(ListProduct, self).get_queryset(*args, **kwargs)
        return self.request.user.product_set.all()


# def shop_delete(request, pk):
#     """
#         this contains function shop delete
#     """
#     print(pk)
#     user_objects = User.objects.get(id=pk)
#     print(user_objects)
#     user_objects.delete()
#     print('success')
#     return HttpResponse('successfully deleted')


class ShopProductDelete(DeleteView):
    """
        this contains function shop delete
    """
    model = User

    def get_success_url(self):
        return reverse('ecomapp:ecomdash')


def product_delete(request, pk):
    """
        this contains function product delete
    """
    print(pk)
    user_objects = Product.objects.get(id=pk)
    print(user_objects)
    user_objects.delete()
    print('success')
    return HttpResponse('successfully deleted')


class ProductDelete(DeleteView):
    """
        this contains function product delete
    """
    print("delete-product")
    model = Product
    success_url = '/listproduct/'


@login_required
def update_product(request, pk):
    """
        this contains function update product details
    """
    print(pk)
    # current_user = request.user
    # print(current_user)
    # order = Customuser.objects.get(id=pk)
    # print(order)
    obj = get_object_or_404(Product, id=pk)
    print(obj)
    form = Addproduct(request.POST or None, instance=obj)
    # form = UpdateForm(instance=order)
    # print(form)
    # if request.method == 'POST':
    #     print("post")
    #     form = UpdateForm(request.POST, order)
    if form.is_valid():
        print("sucess")
        form.save()
        return HttpResponse('success')
    context = {'form': form}
    print("get")
    return render(request, 'ecomapp/product_update.html', context)


class UpdateProduct(View):
    """
        this contains function update product details
    """

    def get(self, request, pk):
        obj = get_object_or_404(Product, id=pk)
        print(obj)
        form = Addproduct(instance=obj)
        context = {'form': form}
        return render(request, 'ecomapp/product_update.html', context)

    def post(self, request, pk):
        obj = get_object_or_404(Product, id=pk)
        print(obj)
        form = Addproduct(request.POST or None, instance=obj)
        if form.is_valid():
            print("sucess")
            form.save()
        return HttpResponse('success')


@login_required
def add_to_wishlist(request, pk):
    """
        this contains function add product ot wish list
    """
    print(pk)
    # import pdb
    # pdb.set_trace()
    current_customer = request.user
    print(current_customer.id)
    wishlist = Wishlist.objects.get(user_id=current_customer.id)
    products = Product.objects.get(id=pk)
    print(products)
    if WishItems.objects.filter(product_id=pk).exists():
        return HttpResponse("Addedd")
    else:
        wishitem = WishItems(wishlist=wishlist, product=products)
        wishitem.save()
    print(wishitem)
    return HttpResponse("Addedd")


class AddToWishlist(View):
    """
        this contains function add product ot wish list
    """
    template_name = 'ecomapp/wishlist.html'

    def post(self, request, pk):
        wishlist = Wishlist.objects.get(user_id=self.request.user.id)
        products = Product.objects.get(id=pk)
        if WishItems.objects.filter(product_id=pk).exists():
            return HttpResponse("Addedd")
        else:
            wishitem = WishItems(wishlist=wishlist, product=products)
            wishitem.save()
        print(wishitem)
        return HttpResponse("Success")


@login_required
def add_to_cart(request, pk, size, color):
    """
        this contains function do add to cart in the project
    """
    print(pk)
    print(size)
    print(color)
    current_customer = request.user
    print(current_customer.id)
    wishlist = Wishlist.objects.get(user_id=current_customer.id)
    print(CartItems.objects.filter(wishlist_id=wishlist.id).exists())
    products = Product.objects.get(id=pk)
    print(products)

    # if CartItems.objects.filter(wishlist_id=wishlist.id).exists() and
    # CartItems.objects.filter(
    # product_id=pk).exists():
    # print("Items if") CartItems.objects.filter(product_id=pk).update(color=color,
    # size=size) return HttpResponse("Addedd")

    cartitem = CartItems(wishlist=wishlist, product=products, color=color, size=size)
    cartitem.save()
    print(cartitem)
    return HttpResponse("Addedd")


class AddToCart(View):
    """
        this contains function do add to cart in the project
    """
    template_name = 'ecomapp/wishlist.html'

    def post(self, request, pk, size, color):
        wishlist = Wishlist.objects.get(user_id=self.request.user.id)
        products = Product.objects.get(id=pk)
        cartitem = CartItems(wishlist=wishlist, product=products, color=color, size=size)
        cartitem.save()
        print(cartitem)
        return HttpResponse("Success")


@login_required
def go_to_wishlist(request):
    """
        this contains function customer can go in the wishlist
    """
    # Version 1
    current_user = request.user
    # user = User.objects.get(id=current_user.id)
    data = current_user.wishlist.wishitems_set.all()
    return render(request, 'ecomapp/wishlist.html', {'data': data})


class GoToWishlist(ListView):
    """
        this contains function customer can go in the wishlist
    """
    # specify the model for list view
    model = WishItems
    template_name = 'ecomapp/wishlist.html'

    def get_queryset(self, *args, **kwargs):
        # context = super(ListProduct, self).get_queryset(*args, **kwargs)
        return self.request.user.wishlist.wishitems_set.all()


@login_required
def go_to_cart(request):
    """
        this contains function go to your cart in the function
    """
    current_user = request.user
    # user = User.objects.get(id=current_user.id)
    print(current_user)
    data = current_user.wishlist.cartitems_set.all()
    product_price = CartItems.objects.filter(wishlist__user=current_user) \
        .aggregate(Sum('product__price'))
    total_price = product_price['product__price__sum']
    print(product_price['product__price__sum'])
    return render(request, 'ecomapp/cartlist.html', {'data': data, 'product__price': total_price})


class GoToCart(ListView):
    """
        this contains function go to your cart in the function
    """
    model = CartItems
    template_name = 'ecomapp/cartlist.html'

    def get_context_data(self, *args, **kwargs):
        context = super(GoToCart, self).get_context_data(*args, **kwargs)
        data = self.request.user.wishlist.cartitems_set.all()
        product_price = CartItems.objects.filter(wishlist__user=self.request.user) \
            .aggregate(Sum('product__price'))
        total_price = product_price['product__price__sum']
        context = {'data': data, 'product_price': total_price}
        print(context)
        return context


def remove_from_wishlist_function(request, pk):
    """
        this contains function re move product from wish list
    """
    print(pk)
    print(WishItems)

    print(WishItems)


class RemoveProductWishlist(View):
    """
        this contains function re move product from wish list
    """

    def post(self, request, pk):
        WishItems.objects.filter(id=pk).delete()
        return HttpResponse("Addedd")


def remove_from_cart_function(request, pk):
    """
        this contains function remove from cart functions
    """
    print(pk)
    print(CartItems)
    CartItems.objects.filter(id=pk).delete()
    print(CartItems)
    return HttpResponse("Addedd")


class RemoveProductFromCart(View):
    """
        this contains function remove from cart functions
    """

    def post(self, request, pk):
        CartItems.objects.filter(id=pk).delete()
        return HttpResponse("Addedd")


def add_to_my_orders(request):
    """
        this contains function add to my orders
    """
    current_customer = request.user
    wishlist = Wishlist.objects.get(user_id=current_customer.id)
    cartitems = CartItems.objects.filter(wishlist__user=request.user.id)
    for items in cartitems:
        user = Product.objects.get(id=items.product_id).user
        # print(user)
        myorder = MyOrders(wishlist=wishlist, quantity=items.quantity, user=user,
                           product_id=items.product_id,
                           product_type=items.product.product_type,
                           product_name=items.product.product_name,
                           price=items.product.price,
                           size=items.size, color=items.color,
                           product_img=items.product.product_img,
                           gender=items.product.gender)
        myorder.save()
    CartItems.objects.all().delete()
    return HttpResponse("Placed")


class AddToMyOrders(View):
    """
        this contains function add to my orders
    """
    template_name = 'ecomapp/wishlist.html'

    def post(self, request):
        wishlist = Wishlist.objects.get(user_id=self.request.user.id)
        cartitems = CartItems.objects.filter(wishlist__user=self.request.user.id)
        for items in cartitems:
            user = Product.objects.get(id=items.product_id).user
            myorder = MyOrders(wishlist=wishlist, quantity=items.quantity, user=user,
                               product_id=items.product_id,
                               product_type=items.product.product_type,
                               product_name=items.product.product_name,
                               price=items.product.price,
                               size=items.size, color=items.color,
                               product_img=items.product.product_img,
                               gender=items.product.gender)
            myorder.save()

        CartItems.objects.all().delete()
        return HttpResponse("Success")


def go_to_your_order(request):
    """
        this contains function customer go to there orders
    """
    current_user = request.user
    myorder = current_user.wishlist.myorders_set.all()
    return render(request, 'ecomapp/myorders_page.html', {'myorder': myorder})


class GoToYourOrder(ListView):
    """
        this contains function customer go to there orders
    """
    # specify the model for list view
    model = MyOrders
    template_name = 'ecomapp/myorders_page.html'

    def get_queryset(self, *args, **kwargs):
        # context = super(ListProduct, self).get_queryset(*args, **kwargs)
        return self.request.user.wishlist.myorders_set.all()


def remove_from_order(request, pk):
    """
        this contains function remove product from order list
    """
    # myorder = MyOrders.objects.get(id=id)
    MyOrders.objects.filter(id=pk).delete()
    return HttpResponse("Removed")


class RemoveProductFromOrder(View):
    """
        this contains function remove product from order list
    """

    def post(self, request, pk):
        MyOrders.objects.filter(id=pk).delete()
        return HttpResponse("Addedd")


def update_order_quantity(request, pk, quantity):
    """
        this contains function updates order quantity
    """
    # myorder = MyOrders.objects.get(id=id)
    # MyOrders.objects.filter(id=pk).delete()
    CartItems.objects.filter(id=pk).update(quantity=quantity)
    # update.save()
    return HttpResponse("Updated")


class UpdateCartQuantity(View):
    """
        this contains function updates order quantity
    """

    def post(self, request, pk, quantity):
        CartItems.objects.filter(id=pk).update(quantity=quantity)
        return HttpResponse("Addedd")


# class RemoveProductFromOrder(View):
#
#     def post(self, request, pk):
#         MyOrders.objects.filter(id=pk).delete()
#         return HttpResponse("Addedd")


def shop_orders(request):
    """
        this contains function shop orders
    """
    current_shop = request.user
    print(current_shop.id)
    products = MyOrders.objects.filter(user_id=current_shop.id)
    print(products)
    # print(products[0].wishlist.user.username)
    return render(request, 'ecomapp/shop_orders.html', {'products': products})


class ShopOrders(ListView):
    """
        this contains function shop orders
    """
    # specify the model for list view
    model = Product
    template_name = 'ecomapp/shop_orders.html'

    def get_queryset(self, *args, **kwargs):
        # context = super(ListProduct, self).get_queryset(*args, **kwargs)
        return MyOrders.objects.filter(user_id=self.request.user.id)


def final_address(request):
    """
        this contains function final address to the customer were we can deliver
    """
    current_user = request.user
    print(current_user)
    print(current_user.id)
    obj = get_object_or_404(User, id=current_user.id)
    print(obj)
    form = FinalAddress(request.POST or None, instance=obj)
    print(form)
    context = {'form': form}
    print(context)
    if request.method == 'GET':
        return render(request, 'ecomapp/final_address.html', context)
    elif request.method == "POST":
        # print("hereeeee post", data)
        # User.objects.filter(id=request.POST)
        if form.is_valid():
            print("sucess")
            form.save()
            # return HttpResponse('success')
        return render(request, 'ecomapp/final_address.html', context)


class FinalAddressDetails(View):
    """
        this contains function final address to the customer were we can deliver
    """

    def get(self, request):
        obj = get_object_or_404(User, id=self.request.user.id)
        print(obj)
        form = FinalAddress(instance=obj)
        context = {'form': form}
        return render(request, 'ecomapp/final_address.html', context)

    def post(self, request):
        obj = get_object_or_404(User, id=self.request.user.id)
        print(obj)
        form = FinalAddress(request.POST or None, instance=obj)
        if form.is_valid():
            print("sucess")
            form.save()
        return HttpResponse('success')


def list_product_admin(request, pk):
    """
        this contains function list of products on the admin page
    """
    user_product = User.objects.get(id=pk) \
        .product_set.all()
    # print(user_product)
    return render(request, 'ecomapp/shopuser_list_admin.html',
                  {'user_product': user_product, 'id': pk})


class ProductListAdmin(TemplateView):
    """
        this contains function list of products on the admin page
    """
    template_name = 'ecomapp/shopuser_list_admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(kwargs)
        context['user_product'] = User.objects.get(id=kwargs['pk']).product_set.all()
        context['id'] = kwargs['pk']
        print(context)
        return context


def shop_orders_admin(request, pk):
    """
        this contains function shop orders from admin
    """
    # current_shop = request.user
    products = MyOrders.objects.filter(user_id=pk)
    print(products)
    # print(products[0].wishlist.user.username)
    return render(request, 'ecomapp/shop_orders.html', {'products': products})


class ShopOrderAdmin(TemplateView):
    """
        this contains function shop orders from admin
    """
    template_name = 'ecomapp/shop_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(kwargs)
        context['object_list'] = MyOrders.objects.filter(user_id=kwargs['pk'])
        print(context)
        return context


@login_required
def all_customers_admin(request):
    """
        this contains function all customers admin
    """
    current_user = request.user
    print("all customers")
    if current_user.user_type == 'admin':
        print("dffdd")
        all_customers = User.objects.filter(user_type='customer')
        print(all_customers)
        return render(request, 'ecomapp/all_customer_admin.html', {'all_customers': all_customers})
    return HttpResponse("Login Required")


class AllCustomersAdmin(ListView):
    """
        this contains function all customers admin
    """
    # specify the model for list view
    model = User
    template_name = 'ecomapp/all_customer_admin.html'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.user_type == 'admin':
            return User.objects.filter(user_type='customer')
        return HttpResponse("Login Required")


def go_to_your_order_admin(request, pk):
    """
        this contains function customers orders in admins
    """
    myorder = User.objects.get(id=pk).wishlist.myorders_set.all()
    return render(request, 'ecomapp/myorders_page.html', {'myorder': myorder})


class GoToCustomerOrderAdmin(TemplateView):
    """
        this contains function customers orders in admins
    """
    template_name = 'ecomapp/myorders_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(kwargs)
        context['object_list'] = User.objects.get(user_id=kwargs['pk']).wishlist.myorders_set.all()
        print(context)
        return context


def product_sales(request, pk, pk1):
    """
        this contains function product sales
    """
    # import pdb;pdb.set_trace()
    # print(pk)
    # print(pk1)
    total_shell_product = User.objects.get(id=pk1).product_set.filter(id=pk).aggregate(Sum('quantity'))
    print(total_shell_product)
    total_order_recieved = MyOrders.objects.filter(product_id=pk).aggregate(Sum('quantity'))
    print(total_order_recieved)
    if total_order_recieved['quantity__sum'] is None:
        total_sell = 0
    else:
        total_sell = (total_order_recieved['quantity__sum']
                      / total_shell_product['quantity__sum']) * 100
    print(total_sell)
    return JsonResponse({'total_product_sell': total_sell})


class ProductSalesAdmin(View):
    """
        this contains function product sales
    """
    template_name = 'ecomapp/shopuser_list_admin.html'

    def get(self, request, *args, **kwargs):
        print(kwargs)
        total_shell_product = User.objects.get(id=kwargs['pk1']).product_set.filter(id=kwargs['pk']).aggregate(
            Sum('quantity'))
        print(total_shell_product)
        total_order_recieved = MyOrders.objects.filter(product_id=kwargs['pk']).aggregate(Sum('quantity'))
        print(total_order_recieved)
        if total_order_recieved['quantity__sum'] is None:
            total_sell = 0
        else:
            total_sell = (total_order_recieved['quantity__sum']
                          / total_shell_product['quantity__sum']) * 100
        return JsonResponse({'total_product_sell': total_sell})
