import pdb

from allauth.account.forms import SignupForm
from allauth.account.utils import user_field
from django import forms
from allauth.account.adapter import get_adapter
# from .utils import user_email, user_field, user_username
from ecomapp.models import User, Product, CartItems, Variations


class CustomSignupForm(SignupForm):
    full_name = forms.CharField(max_length=30, label='First Name')
    gender = forms.CharField(max_length=30, label='Gender')
    mobile = forms.CharField(max_length=11)
    Address = forms.CharField(max_length=50)

    def save(self, request):
        # breakpoint()
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        adapter.save_user(request, user, self, commit=False)

        # user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['full_name']
        user.account_type = 1
        # user.DOB = self.clened_data['DOB']
        user.gender = self.cleaned_data['gender']
        user.mobile_no = self.cleaned_data['mobile']
        user.addressof_customer = self.cleaned_data['Address']
        user.user_type = 'customer'
        user.is_active = True
        user.save()
        print(user.__dict__)
        return user

    class Meta:
        model = User
        fields = ['email', 'full_name', 'username', 'gender', 'password', 'mobile_no', 'addressof_customer']


class ShopSignupForm(SignupForm):
    Brand = forms.CharField(max_length=30, label='Brand Name')
    shop_name = forms.CharField(max_length=40, label='shop name')
    mob = forms.CharField(max_length=11)

    def save(self, request):
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        adapter.save_user(request, user, self, commit=False)
        # user = super(CustomSignupForm, self).save(request)
        user.Brand = self.cleaned_data['Brand']
        # user.DOB = self.clened_data['DOB']
        user.account_type = 1
        user.shop_name = self.cleaned_data['shop_name']
        user.user_type = 'shopuser'
        user.is_active = False
        user.save()
        print(user.__dict__)
        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'Brand', 'shop_name', 'password']


class UpdateForm(forms.ModelForm):
    # full_name = forms.CharField(max_length=30, label='first_name')
    # DOB = forms.DateField()
    gender = forms.CharField(max_length=30, label='gender', widget=forms.TextInput(attrs={"type": "text",
                                                                                          "class": "form-control",
                                                                                          "id": "inputgender",
                                                                                          "placeholder": "gender"}))

    # usertype = forms.ChoiceField(choices=users)

    # def save(self, request):
    #     # breakpoint()
    #     user = super(UpdateForm, self).save(request)
    #     user.first_name = self.cleaned_data['full_name']
    #     user.user_type = self.cleaned_data['usertype']
    #     # user.DOB = self.clened_data['DOB']
    #     user.gender = self.cleaned_data['gender']
    #     user.save()
    #     return user

    class Meta:
        model = User
        fields = ['email', 'first_name', 'username', 'gender']
        widgets = {
            'email': forms.TextInput(attrs={
                "type": "email",
                "class": "form-control",
                "id": "inputEmail4",
                "placeholder": "Email"
            }),
            'first_name': forms.TextInput(attrs={
                "type": "text",
                "class": "form-control",
                "id": "inputFirstname",
                "placeholder": "first name"
            }),
            'username': forms.TextInput(attrs={
                "type": "text",
                "class": "form-control",
                "id": "inputusername",
                "placeholder": "username"
            }),
            'gender': forms.TextInput(attrs={
                "type": "text",
                "class": "form-control",
                "id": "inputgender",
                "placeholder": "gender"
            })
        }


class CreatShopUser(forms.ModelForm):
    gender = forms.CharField(max_length=30, label='gender', widget=forms.TextInput(attrs={"type": "text",
                                                                                          "class": "form-control",
                                                                                          "id": "inputgender",
                                                                                          "placeholder": "gender"}))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'username', 'gender']
        widgets = {
            'email': forms.TextInput(attrs={
                "type": "email",
                "class": "form-control",
                "id": "inputEmail4",
                "placeholder": "Email"
            }),
            'first_name': forms.TextInput(attrs={
                "type": "text",
                "class": "form-control",
                "id": "inputFirstname",
                "placeholder": "first name"
            }),
            'username': forms.TextInput(attrs={
                "type": "text",
                "class": "form-control",
                "id": "inputusername",
                "placeholder": "username"
            }),
            'gender': forms.TextInput(attrs={
                "type": "text",
                "class": "form-control",
                "id": "inputgender",
                "placeholder": "gender"
            })
        }


gender = (
    ('male', 'male'),
    ('female', 'female'))


class Addproduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_type', 'product_name', 'description', 'gender', 'price', 'product_img']


class FinalAddress(forms.ModelForm):

    class Meta:
        model = User
        fields = ['mobile_no', 'addressof_customer']
