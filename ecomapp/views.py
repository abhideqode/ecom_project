"""
   this contains all the functions in it
   """
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse


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


def newshop_user(request):
    """
        this contains new shop user in django
        we can add data
     """
    form = ShopSignupForm(request.POST or None)
    if form.is_valid():
        form.save(request)
        return render(request, 'account/account_inactive.html')
    context = {'form': form}
    return render(request, 'account/shop_user.html', context)


def update_order(request, pk):
    """
        this contains update order
        data
    """
    obj = get_object_or_404(User, id=pk)
    print(obj)
    form = UpdateForm(request.POST or None, instance=obj)
    context = {'form': form}
    print(context)
    if request.method == 'GET':
        return render(request, 'ecomapp/update.html', context)
    elif request.method == "POST":
        # print("hereeeee post", data)
        # User.objects.filter(id=request.POST)
        if form.is_valid():
            print("sucess")
            form.save()
            # return HttpResponse('success')
        return render(request, 'ecomapp/update.html', context)
        # form = UpdateForm(instance=order)
    # print(form)
    # if request.method == 'POST':
    #     print("post")
    #     form = UpdateForm(request.POST, order)
    #
    # print("get")
    # return render(request, 'ecomapp/update.html', context)


def shop_user(request):
    """
        this contains function shop users
    """
    form = ShopUser(request.POST or None)
    if form.is_valid():
        form.save(request)
    context = {'form': form}

    return render(request, 'ecomapp/shopregis.html', context)


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


def request_list(request):
    """
        this contains function request llist for users
    """
    print("requestlist")
    users_list = User.objects.filter(is_active=False)

    return render(request, 'ecomapp/adminrequest.html', {'context': users_list})


@login_required
def shop_list(request):
    """
         this contains function shop list for users
     """
    current_user = request.user
    if current_user.user_type == 'admin':
        shop_user_list = User.objects.filter(is_active=True, user_type='shopuser')
        return render(request, 'ecomapp/shopuserlist.html', {'context': shop_user_list})
    return HttpResponse("Login Required")


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


@login_required
def list_product(request):
    """
        this contains function list of product
    """
    current_user = request.user
    user_product = current_user.product_set.all()
    return render(request, 'ecomapp/product_list.html', {'context': user_product})


def shop_delete(request, pk):
    """
        this contains function shop delete
    """
    print(pk)
    user_objects = User.objects.get(id=pk)
    print(user_objects)
    user_objects.delete()
    print('success')
    return HttpResponse('successfully deleted')


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


def remove_from_wishlist_function(request, pk):
    """
        this contains function re move product from wish list
    """
    print(pk)
    print(WishItems)
    WishItems.objects.filter(id=pk).delete()
    print(WishItems)
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


def go_to_your_order(request):
    """
        this contains function customer go to there orders
    """
    current_user = request.user
    myorder = current_user.wishlist.myorders_set.all()
    return render(request, 'ecomapp/myorders_page.html', {'myorder': myorder})


def remove_from_order(request, pk):
    """
        this contains function remove product from order list
    """
    # myorder = MyOrders.objects.get(id=id)
    MyOrders.objects.filter(id=pk).delete()
    return HttpResponse("Removed")


def update_order_quantity(request, pk, quantity):
    """
        this contains function updates order quantity
    """
    # myorder = MyOrders.objects.get(id=id)
    # MyOrders.objects.filter(id=pk).delete()
    CartItems.objects.filter(id=pk).update(quantity=quantity)
    # update.save()
    return HttpResponse("Updated")


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


def list_product_admin(request, pk):
    """
        this contains function list of products on the admin page
    """
    user_product = User.objects.get(id=pk) \
        .product_set.all()
    # print(user_product)
    return render(request, 'ecomapp/shopuser_list_admin.html',
                  {'user_product': user_product, 'id': pk})


def shop_orders_admin(request, pk):
    """
        this contains function shop orders from admin
    """
    # current_shop = request.user
    products = MyOrders.objects.filter(user_id=pk)
    print(products)
    # print(products[0].wishlist.user.username)
    return render(request, 'ecomapp/shop_orders.html', {'products': products})


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


def go_to_your_order_admin(request, pk):
    """
        this contains function product go to your orders admins
    """
    myorder = User.objects.get(id=pk).wishlist.myorders_set.all()
    return render(request, 'ecomapp/myorders_page.html', {'myorder': myorder})


def product_sales(request, pk, pk1):
    """
        this contains function product sales
    """
    # import pdb;pdb.set_trace()
    # print(pk)
    # print(pk1)
    total_shell_product = User.objects.get(id=pk1). \
        product_set.filter(id=pk).aggregate(Sum('quantity'))
    print(total_shell_product)
    total_order_recieved = MyOrders.objects.filter(product_id=pk).aggregate(Sum('quantity'))
    print(total_order_recieved)
    if total_order_recieved['quantity__sum'] is None:
        total_product_sell = 0
    else:
        total_sell = (total_order_recieved['quantity__sum']
                      / total_shell_product['quantity__sum']) * 100
    print(total_product_sell)
    return JsonResponse({'total_product_sell': total_sell})
