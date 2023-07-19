#import form
from django import forms
#registration form
from django.contrib.auth.forms import UserCreationForm
#to store the details in DB
from django.contrib.auth.models import User
#for login and UsernameField: login by using username during registration
from django.contrib.auth.forms import AuthenticationForm, UsernameField
#standard translation related to password(to maintain password structure(space/etc))
from django.utils.translation import gettext, gettext_lazy as _
#import password change form
from django.contrib.auth.forms import PasswordChangeForm
#to validate the old/existing password
from django.contrib.auth import password_validation
#passwordreset form
from django.contrib.auth.forms import PasswordResetForm
#Set new password 
from django.contrib.auth.forms import SetPasswordForm
#Customer profile model import
from .models import Customer


#Registration and form-control: bootstrap beautification
class CustomerRegistrationForm(UserCreationForm):

    #password
    #bootstrap class: {'class': 'form-control'}
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    #confirm password
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))

    #to save data into DB 
    class Meta:
        #User table
        model = User
        #views on front end and DB fields
        fields = ['username', 'email', 'password1', 'password2']

        #modified labels
        labels = {'email': 'Email'}

        widgets = {'username': forms.TextInput(attrs={'class':'form-control'})}

#user login and form-control: bootstrap beautification
class LoginForm(AuthenticationForm):
    username = UsernameField(widget= forms.TextInput(attrs= {'autofocus': True, 'class': 'form-control'}))
    #strip:False, keeps the password as it is. 
    password = forms.CharField(label = ('Password'), strip = False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control'}))

#Password Change form(strip:False; don't remove space in password). _ (underscore) for standard translation
class DoChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label=_('Old Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'autofocus': True, 'class':'form-control'}))

    new_password1 = forms.CharField(label=_('New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())


    new_password2 = forms.CharField(label=_('Confirm New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new password', 'class':'form-control'}))

#forget password _ (underscore) for standard translation
#step-1: reset
class DoPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label = _("Email"), max_length = 250, widget = forms.EmailInput(attrs= {'autocomplet': 'email', 'class': 'form-control'}))

#step-3: set password
class DoSetPasswordConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_('New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_('Confirm New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new password', 'class':'form-control'}))

#create customer profile form
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields= ['name', 'division', 'district', 'thana', 'villorroad', 'zipcode']
        #form-control: bootstrap class. 
        widgets ={
            'name': forms.TextInput(attrs= {'class' : 'form-control'}),
            #select as per tuple
            'division' : forms.Select(attrs={'class' : 'form-control'}),
            'district' : forms.TextInput(attrs={'class' : 'form-control'}),
            'thana' : forms.TextInput(attrs={'class' : 'form-control'}),
            'villorroad' : forms.TextInput(attrs={'class' : 'form-control'}),
            'zip' : forms.NumberInput(attrs={'class' : 'form-control'}),}




