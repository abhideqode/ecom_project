from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView

from .models import User
from .form import UpdateForm, CustomSignupForm, ShopUser


# Create your views here.
@login_required
def test(request):
    t = User.objects.all()
    current_user = request.user
    print(current_user)
    return render(request, 'ecomapp/home.html', {'t': current_user})


def updateOrder(request, pk):
    print(pk)
    current_user = request.user
    # print(current_user)
    # order = Customuser.objects.get(id=pk)
    # print(order)
    obj = get_object_or_404(User, id=pk)
    print(obj)
    form = UpdateForm(request.POST or None, instance=obj)
    # form = UpdateForm(instance=order)
    print(form)
    # if request.method == 'POST':
    #     print("post")
    #     form = UpdateForm(request.POST, order)
    if form.is_valid():
        print("sucess")
        form.save()
        return redirect('ecomdash')
    context = {'form': form}
    print("get")
    return render(request, 'ecomapp/update.html', context)


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
