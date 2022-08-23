import pdb

from allauth.account.forms import SignupForm
from allauth.account.utils import user_field
from django import forms
from allauth.account.adapter import get_adapter
# from .utils import user_email, user_field, user_username
from ecomapp.models import User


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
        user.is_active = user.user_type == self.users[0][0]
        user.save()
        print(user.__dict__)
        return user

    class Meta:
        model = User
        fields = ['email', 'full_name', 'user_type', 'username', 'gender', 'password']


class UpdateForm(forms.ModelForm):
    users = (
        ('admin', 'admin'),
        ('shopuser', 'shopuser'),
        ('customer', 'customer')
    )

    full_name = forms.CharField(max_length=30, label='First Name')
    # DOB = forms.DateField()
    gender = forms.CharField(max_length=30, label='Gender')
    usertype = forms.ChoiceField(choices=users)

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
        fields = ['email', 'full_name', 'username', 'gender', 'password']


class ShopUser(SignupForm):
    shop_name = forms.CharField(max_length=40)
    is_active = 'False'

    # shop_email = forms.EmailField(max_length=40, blank=True)

    class Meta:
        model = User
        fields = ['email', 'shop_name', 'password']

# from django import forms
# from .models import Customuser
# class SignForm(forms.ModelForm):

#     username = forms.CharField(
#         max_length=30,
#     )

#     def myclean():
#         pass
#     def signup(self, request, user):
#         """You signup function."""

#     class Meta:
#         model = Customuser
#         fields = [
#             'usertype'
#         ]
