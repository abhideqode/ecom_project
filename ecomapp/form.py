"""
     this form.py file is for the different form for the user
 """
from allauth.account.forms import SignupForm
# from allauth.account.utils import user_field
from django import forms
from allauth.account.adapter import get_adapter
# from .utils import user_email, user_field, user_username
from ecomapp.models import User, Product


class CustomSignupForm(SignupForm):
    """
         this class is for the Customer signup form
     """
    full_name = forms.CharField(max_length=30, label='First Name')
    gender = forms.CharField(max_length=30, label='Gender')
    mobile = forms.CharField(max_length=11)
    Address = forms.CharField(max_length=50)

    def save(self, request):
        """
             this is save function for the custom signup form
         """
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
        """
             this is the meta class for the customer signup form
         """
        model = User
        fields = ['email', 'full_name', 'username', 'gender',
                  'password', 'mobile_no', 'addressof_customer']


class ShopSignupForm(SignupForm):
    """
         this is class for the shop signup form
     """
    Brand = forms.CharField(max_length=30, label='Brand Name')
    shop_name = forms.CharField(max_length=40, label='shop name')
    mob = forms.CharField(max_length=11)

    def save(self, request):
        """
             this is save function for the shop signup form
         """
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
        """
             this is the meta class for the Signup ofr the shopuser
         """
        model = User
        fields = ['username', 'email', 'Brand', 'shop_name', 'password']


class UpdateForm(forms.ModelForm):
    """
         this is class for the update signup form
     """
    # full_name = forms.CharField(max_length=30, label='first_name')
    # DOB = forms.DateField()
    gender = forms.CharField(max_length=30,
                             label='gender',
                             widget=forms.TextInput(attrs={"type": "text",
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
        """
             this is the meta class for the update product form
         """
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
    """
         this is class for the Create shop user form
     """
    gender = forms.CharField(max_length=30, label='gender',
                             widget=forms.TextInput(attrs={"type": "text",
                                                           "class": "form-control",
                                                           "id": "inputgender",
                                                           "placeholder": "gender"}))

    class Meta:
        """
             this is the meta class for the create shop user
         """
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


Gender = (
    ('male', 'male'),
    ('female', 'female'))


class Addproduct(forms.ModelForm):
    """
        this is the claas for the add product form
    """

    class Meta:
        """
            this is the meta class for the add product form
        """
        model = Product
        fields = ['product_type', 'product_name',
                  'description', 'gender',
                  'price', 'product_img']


class FinalAddress(forms.ModelForm):
    """
        this is the final address form for project app
    """

    class Meta:
        """
            this is the meta class for the final address
        """
        model = User
        fields = ['mobile_no', 'addressof_customer']
