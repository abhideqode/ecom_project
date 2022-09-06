from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from django.views.generic import UpdateView

from .models import User, Product, Wishlist, WishItems, CartItems, MyOrders
from .form import UpdateForm, CustomSignupForm, CreatShopUser, Addproduct, ShopSignupForm, FinalAddress

total = 0


# Create your views here.
@login_required
def test(request):
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
        total_order_recieved = MyOrders.objects.filter(user_id=current_user.id).aggregate(Sum('quantity'))
        total_product_sell = (total_order_recieved['quantity__sum'] / total_shell_product['quantity__sum']) * 100
        print(total_product_sell)
        return render(request, 'ecomapp/shopuser.html', {'t': current_user, 'total_product_sell': total_product_sell})
    elif user.user_type == 'customer':
        return render(request, 'ecomapp/customer.html', {'t': current_user, 'products': products})

    print("current_user")
    print(current_user)


def newshop_user(request):
    form = ShopSignupForm(request.POST or None)
    if form.is_valid():
        form.save(request)
        return render(request, 'account/account_inactive.html')
    context = {'form': form}
    return render(request, 'account/shop_user.html', context)


def updateOrder(request, pk):
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


def shopuser(request):
    form = ShopUser(request.POST or None)
    if form.is_valid():
        form.save(request)
    context = {'form': form}

    return render(request, 'ecomapp/shopregis.html', context)


def shopuserApp(request, pk):
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


def requestlist(request):
    print("requestlist")
    u = User.objects.filter(is_active=False)
    print(u)
    return render(request, 'ecomapp/adminrequest.html', {'context': u})


@login_required
def shoplist(request):
    c = request.user
    if c.user_type == 'admin':
        u = User.objects.filter(is_active=True, user_type='shopuser')
        return render(request, 'ecomapp/shopuserlist.html', {'context': u})
    return HttpResponse("Login Required")


def createshopuser(request):
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
            p = User(email=email, first_name=first_name, username=username, gender=gender, user_type='shopuser')
            p.save()
            return HttpResponse('Saved')
        # if a GET (or any other method) we'll create a blank form
    else:
        form = CreatShopUser()

    return render(request, 'ecomapp/createshopuser.html', {'form': form})


def addproduct(request):
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
    current_user = request.user
    user_product = current_user.product_set.all()
    return render(request, 'ecomapp/product_list.html', {'context': user_product})


def shopdelete(request, pk):
    print(pk)
    u = User.objects.get(id=pk)
    print(u)
    u.delete()
    print('success')
    return HttpResponse('successfully deleted')


def productdelete(request, pk):
    print(pk)
    u = Product.objects.get(id=pk)
    print(u)
    u.delete()
    print('success')
    return HttpResponse('successfully deleted')


@login_required
def updateproduct(request, pk):
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
def addtowishlist(request, pk):
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
def addtocart(request, pk, size, color):
    print(pk)
    print(size)
    print(color)
    current_customer = request.user
    print(current_customer.id)
    wishlist = Wishlist.objects.get(user_id=current_customer.id)
    print(CartItems.objects.filter(wishlist_id=wishlist.id).exists())
    products = Product.objects.get(id=pk)
    print(products)

    # if CartItems.objects.filter(wishlist_id=wishlist.id).exists() and CartItems.objects.filter(
    # product_id=pk).exists(): print("Items if") CartItems.objects.filter(product_id=pk).update(color=color,
    # size=size) return HttpResponse("Addedd")

    cartitem = CartItems(wishlist=wishlist, product=products, color=color, size=size)
    cartitem.save()
    print(cartitem)
    return HttpResponse("Addedd")


@login_required
def go_to_wishlist(request):
    # Version 1
    current_user = request.user
    # user = User.objects.get(id=current_user.id)
    data = current_user.wishlist.wishitems_set.all()
    return render(request, 'ecomapp/wishlist.html', {'data': data})


@login_required
def go_to_cart(request):
    current_user = request.user
    # user = User.objects.get(id=current_user.id)
    print(current_user)
    data = current_user.wishlist.cartitems_set.all()
    product__price = CartItems.objects.filter(wishlist__user=current_user).aggregate(Sum('product__price'))
    total = product__price['product__price__sum']
    print(product__price['product__price__sum'])
    return render(request, 'ecomapp/cartlist.html', {'data': data, 'product__price': total})


def remove_from_wishlist_function(request, pk):
    print(pk)
    print(WishItems)
    WishItems.objects.filter(id=pk).delete()
    print(WishItems)
    return HttpResponse("Addedd")


def remove_from_cart_function(request, pk):
    print(pk)
    print(CartItems)
    CartItems.objects.filter(id=pk).delete()
    print(CartItems)
    return HttpResponse("Addedd")


def add_to_my_orders(request):
    current_customer = request.user
    wishlist = Wishlist.objects.get(user_id=current_customer.id)
    cartitems = CartItems.objects.filter(wishlist__user=request.user.id)
    for items in cartitems:
        user = Product.objects.get(id=items.product_id).user
        print(user)
        myorder = MyOrders(wishlist=wishlist, quantity=items.quantity, user=user, product_id=items.product_id,
                           product_type=items.product.product_type, product_name=items.product.product_name,
                           price=items.product.price, size=items.size, color=items.color,
                           product_img=items.product.product_img, gender=items.product.gender)
        myorder.save()
    CartItems.objects.all().delete()
    return HttpResponse("Placed")


def go_to_your_order(request):
    current_user = request.user
    myorder = current_user.wishlist.myorders_set.all()
    return render(request, 'ecomapp/myorders_page.html', {'myorder': myorder})


def remove_from_order(request, pk):
    # myorder = MyOrders.objects.get(id=id)
    MyOrders.objects.filter(id=pk).delete()
    return HttpResponse("Removed")


def update_order_quantity(request, pk, quantity):
    # myorder = MyOrders.objects.get(id=id)
    # MyOrders.objects.filter(id=pk).delete()
    CartItems.objects.filter(id=pk).update(quantity=quantity)
    # update.save()
    return HttpResponse("Updated")


def shop_orders(request):
    current_shop = request.user
    print(current_shop.id)
    products = MyOrders.objects.filter(user_id=current_shop.id)
    print(products)
    # print(products[0].wishlist.user.username)
    return render(request, 'ecomapp/shop_orders.html', {'products': products})


def final_address(request):
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
    user_product = User.objects.get(id=pk).product_set.all()
    print(user_product)
    return render(request, 'ecomapp/shopuser_list_admin.html', {'user_product': user_product, 'id': pk})


def shop_orders_admin(request, pk):
    # current_shop = request.user
    products = MyOrders.objects.filter(user_id=pk)
    print(products)
    # print(products[0].wishlist.user.username)
    return render(request, 'ecomapp/shop_orders.html', {'products': products})


@login_required
def all_customers_admin(request):
    c = request.user
    print("all customers")
    if c.user_type == 'admin':
        print("dffdd")
        all_customers = User.objects.filter(user_type='customer')
        print(all_customers)
        return render(request, 'ecomapp/all_customer_admin.html', {'all_customers': all_customers})
    return HttpResponse("Login Required")


def go_to_your_order_admin(request, pk):
    myorder = User.objects.get(id=pk).wishlist.myorders_set.all()
    return render(request, 'ecomapp/myorders_page.html', {'myorder': myorder})


def product_sales(request, pk, pk1):
    # import pdb;pdb.set_trace()
    print(pk)
    print(pk1)
    total_shell_product = User.objects.get(id=pk1).product_set.filter(id=pk).aggregate(Sum('quantity'))
    print(total_shell_product)
    total_order_recieved = MyOrders.objects.filter(product_id=pk).aggregate(Sum('quantity'))
    print(total_order_recieved)
    if total_order_recieved['quantity__sum'] is None:
        total_product_sell = 0
    else:
        total_product_sell = (total_order_recieved['quantity__sum'] / total_shell_product['quantity__sum']) * 100
    print(total_product_sell)
    return JsonResponse({'total_product_sell':total_product_sell})
