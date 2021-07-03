from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from . models import ShippingAddress


class RegistrationForm(UserCreationForm):
  first_name = forms.CharField(
    max_length=70,
    required=True,
    widget=forms.TextInput(attrs={
      'class':'form-control',
      'placeholder':'First Name',
    })
  )
  last_name = forms.CharField(
    max_length=70,
    required=True,
    widget=forms.TextInput(attrs={
      'class':'form-control',
      'placeholder':'Last Name',
    })
  )
  username = forms.CharField(
    max_length=70,
    required=True,
    widget=forms.TextInput(attrs={
      'class':'form-control',
      'placeholder':'Username',
    })
  )
  email = forms.EmailField(
    label=('Email Id'),
    max_length=70,
    required=True,
    widget=forms.EmailInput(attrs={
      'class':'form-control',
      'placeholder':'Email ID (Not Editable)',
    })
  )
  password1 = forms.CharField(
    strip=False,
    required=True,
    help_text=password_validation.password_validators_help_text_html(),
    widget=forms.PasswordInput(attrs={
      'autocomplete': 'new-password',
      'class':'form-control',
      'placeholder':'Password',
    })
  )
  password2 = forms.CharField(
    required=True,
    strip=False,
    help_text=("Enter the same password as before, for verification."),
    widget=forms.PasswordInput(attrs={
      'autocomplete': 'new-password',
      'class':'form-control',
      'placeholder':'Confirm Password',
    })
  )
  
  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
    field_classes = {'username': UsernameField}

class EditRegistrationForm(forms.ModelForm):
  first_name = forms.CharField(
    max_length=70,
    required=True,
    widget=forms.TextInput(attrs={
      'class':'form-control',
      'placeholder':'First Name',
    })
  )
  last_name = forms.CharField(
    max_length=70,
    required=True,
    widget=forms.TextInput(attrs={
      'class':'form-control',
      'placeholder':'Last Name',
    })
  )
  username = forms.CharField(
    max_length=70,
    required=True,
    widget=forms.TextInput(attrs={
      'class':'form-control',
      'placeholder':'Username',
    })
  )
  
  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'username')
    field_classes = {'username': UsernameField}
    
class LoginForm(AuthenticationForm):
  username = UsernameField(
    label=('Username'),
    widget=forms.TextInput(attrs={'autofocus': True, 'class':'form-control', 'placeholder':'Username'})
      )
  password = forms.CharField(
    label=("Password"),
    strip=False,
    widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control', 'placeholder':'Password '}),
  )


class ShippingAddressForm(forms.ModelForm):
  fname = forms.CharField(
    max_length=100,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'})
  )
  lname = forms.CharField(
    max_length=100,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'})
  )
  mobile_no = forms.IntegerField(
    widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Mobile Number'})
  )
  alternative_mobile_no = forms.IntegerField(
    required=False, widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Mobile Number'})
  )
  country = forms.CharField(
    max_length=70, 
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'})
  )
  address_line1 = forms.CharField(
    max_length=150,
    widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address Line 1'}))
  
  address_line2 = forms.CharField(
    max_length=150,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address Line 2'}))
  
  city = forms.CharField(
    max_length=70,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}))
  
  Zipcode = forms.IntegerField(
    widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'ZipCode'}))
  
  state = forms.CharField(
    max_length=70, 
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}))
  
  
  class Meta:
    model = ShippingAddress
    fields = ('fname', 'lname', 'mobile_no', 'alternative_mobile_no', 'country', 'address_line1','address_line2','city','Zipcode','state')



