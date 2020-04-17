from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import SubscribeRequest

class UserCreateForm(UserCreationForm):

    class Meta():
        fields = ('email','first_name','last_name','password1','password2','ip_address','number_of_queries','status','subscription_plan','company')
        model = get_user_model()

        def __init__(self,*args,**kwargs):
            self.fields['email'].label = 'Email Address'
            self.fields['ip_address'].label = 'IP Address'



class SubscribeRequestForm(forms.ModelForm):

    class Meta():
        model = SubscribeRequest
        fields = ('ip_address','subscription_plan','email','firstname','lastname','company','credit_number','expiry_month',
                  'expiry_year','security_code')


        widgets = {
            'ip_address': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter IP Address'}),
            'subscription_plan': forms.Select(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your email'}),
            'firstname': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your First Name'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Last Name'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Company Name'}),
            'credit_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Credit Card Number'}),
            'expiry_month': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Expire Month'}),
            'expiry_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Expire Year'}),
            'security_code': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Security Code'}),
        }

