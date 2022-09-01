from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView

from .models import User, Product, Wishlist, WishItems, CartItems
from .form import UpdateForm, CustomSignupForm, CreatShopUser, Addproduct, ShopSignupForm

total = 0


# Create your views here.
@login_required
def test(request):
    current_user = request.user
    user = User.objects.get(username=current_user)
    products = Product.objects.all()
    # print(user.__dict__)
    # import pdb;
    # pdb.set_trace()
    if user.user_type == 'admin':
        print("called!")
        return render(request, 'ecomapp/admin.html', {'t': current_user})
    elif user.user_type == 'shopuser':
        return render(request, 'ecomapp/shopuser.html', {'t': current_user})
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
    form = UpdateForm(request.POST or None, instance=obj)
    context = {'form': form}
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
        u = User.objects.filter(is_active=True)
        print(u)

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
    u = current_user.product_set.all()
    print(u)
    return render(request, 'ecomapp/product_list.html', {'context': u})


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
def addtocart(request, pk):
    print(pk)
    # import pdb
    # pdb.set_trace()
    current_customer = request.user
    print(current_customer.id)
    wishlist = Wishlist.objects.get(user_id=current_customer.id)
    products = Product.objects.get(id=pk)
    print(products)
    if CartItems.objects.filter(product_id=pk).exists():
        return HttpResponse("Addedd")
    else:
        cartitem = CartItems(wishlist=wishlist, product=products)
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
    pass
