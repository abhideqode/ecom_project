import pdb

from allauth.account.forms import SignupForm
from allauth.account.utils import user_field
from django import forms
from allauth.account.adapter import get_adapter
# from .utils import user_email, user_field, user_username
from ecomapp.models import User, Product


class CustomSignupForm(SignupForm):
    users = (
        ('admin', 'admin'),
        ('shopuser', 'shopuser'),
        ('customer', 'customer')
    )

    full_name = forms.CharField(max_length=30, label='First Name')
    # DOB = forms.DateField()
    gender = forms.CharField(max_length=30, label='Gender')
    user_type = forms.ChoiceField(choices=users)
    mob = forms.CharField(max_length=11)

    def save(self, request):
        # breakpoint()
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        adapter.save_user(request, user, self, commit=False)

        # user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['full_name']
        user.user_type = self.cleaned_data['user_type']
        # user.DOB = self.clened_data['DOB']
        user.gender = self.cleaned_data['gender']
        print(self.users[2][0])
        user.is_active = user.user_type == self.users[0][0] or user.user_type == self.users[2][0]
        user.save()
        print(user.__dict__)
        return user

    class Meta:
        model = User
        fields = ['email', 'full_name', 'user_type', 'username', 'gender', 'password']


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
        fields = ['product_type', 'product_name', 'description', 'product_size', 'price', 'gender', 'product_img']
        # widgets = {
        #     'product_type': forms.TextInput(attrs={
        #         "type": "email",
        #         "class": "form-control",
        #         "id": "inputEmail4",
        #         "placeholder": "product type"
        #     }),
        #     'product_name': forms.TextInput(attrs={
        #         "type": "text",
        #         "class": "form-control",
        #         "id": "inputFirstname",
        #         "placeholder": " name"
        #     }),
        #     'description': forms.TextInput(attrs={
        #         "type": "text",
        #         "class": "form-control",
        #         "id": "inputusername",
        #         "placeholder": "username"
        #     }),
        #     'product_size': forms.TextInput(attrs={
        #         "type": "text",
        #         "class": "form-control",
        #         "id": "inputgender",
        #         "placeholder": "size"
        #     }),
        #     'price': forms.TextInput(attrs={
        #         "type": "text",
        #         "class": "form-control",
        #         "id": "inputgender",
        #         "placeholder": "price"
        #     }),
        #     'gender': forms.TextInput(attrs={
        #         "type": "text",
        #         "class": "form-control",
        #         "id": "inputgender",
        #         "placeholder": "gender"
        #     }, choices=gender)
        # }
