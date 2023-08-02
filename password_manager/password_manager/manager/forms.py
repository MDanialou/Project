from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


from django.forms import ModelForm
from .models import Password
from allauth.account.forms import LoginForm, SignupForm, ResetPasswordForm, ChangePasswordForm, SetPasswordForm, ResetPasswordKeyForm
from allauth_2fa.forms import TOTPDeviceForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
    max_length=100,
    required = True,
    help_text='Enter Email Address',
    widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    first_name = forms.CharField(
    max_length=100,
    required = True,
    help_text='Enter First Name',
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
    max_length=100,
    required = True,
    help_text='Enter Last Name',
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
    )
    username = forms.CharField(
    max_length=200,
    required = True,
    help_text='Enter Username',
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    password1 = forms.CharField(
    help_text='Enter Password',
    required = True,
    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
    required = True,
    help_text='Enter Password Again',
    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}),
    )
    # check = forms.BooleanField(required = False)
    class Meta:
        model = User
        fields = [
        'username', 'email', 'first_name', 'last_name', 'password1', 'password2'
        ]

class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter password', 'autocomplete': 'current-password'
        })


class CustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter email address'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter password', 'autocomplete': 'new-password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Confirm Password', 'autocomplete': 'new-password'
        })


class CustomPasswordResetForm(ResetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter email address'
        })

class CustomResetPasswordKeyForm(ResetPasswordKeyForm):

    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordKeyForm, self).__init__(*args, **kwargs)
        # self.fields['oldpassword'].widget.attrs.update({
        #     'class': 'form-control', 'placeholder': 'OldPassword'
        # })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'New Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'New Password again'
        })



#2FA

class CustomTOPTDeviceForm(TOTPDeviceForm):

    def __init__(self, *args, **kwargs):
        super(TOTPDeviceForm, self).__init__(*args, **kwargs)
        self.fields['token'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter token'
        })

class AddPasswordForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.instance_pk = kwargs.pop('instance_pk')
        super(AddPasswordForm, self).__init__(*args, **kwargs)

    website_name = forms.CharField(
    max_length=100,
    required = True,
    help_text='Enter Website Name',
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Website Name'}),
    )
    website_url = forms.CharField(
    max_length=100,
    required = True,
    help_text='Enter Website Url',
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Website Url'}),
    )
    username = forms.CharField(
    max_length=100,
    required = True,
    help_text='Enter Username',
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    password1 = forms.CharField(
    max_length=100,
    required = True,
    help_text='Enter Password',
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'password1', 'type': 'password'}),
    )
    password2 = forms.CharField(
    max_length=100,
    required = True,
    help_text='Confirm Password',
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'password2', 'type': 'password'}),
    )
    
    # check = forms.BooleanField(required = False)
    class Meta:
        model = Password
        fields = ['website_name', 'website_url', 'username', 'password1', 'password2']

    def clean(self):
 
        # data from the form is fetched using super function
        super(AddPasswordForm, self).clean()
         
        # extract the username and text field from the data
        website_name = self.cleaned_data.get('website_name')
        website_url = self.cleaned_data.get('website_url')
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if self.instance_pk is None:
        
            if Password.objects.filter(website_name=website_name, user=self.user).exists():
                self._errors['website_name'] = self.error_class([
                    'A password already exists for this website'])
            if Password.objects.filter(website_url=website_url, user=self.user).exists():
                self._errors['website_url'] = self.error_class([
                    'A password already exists for this website'])    
            if password1 != password2:
                self._errors['password2'] = self.error_class([
                    "Passwords don't match"])
            if Password.objects.filter(password=password1, user=self.user).exists():
                self._errors['password1'] = self.error_class([
                    'This password is used on another website'])
        else:
            # User.objects.exclude(pk=request.user.id).filter(username=request.POST['username']).exists()
            if Password.objects.exclude(pk=self.instance_pk).filter(website_name=website_name, user=self.user).exists():
                self._errors['website_name'] = self.error_class([
                    'A password already exists for this website'])
            if Password.objects.exclude(pk=self.instance_pk).filter(website_url=website_url, user=self.user).exists():
                self._errors['website_url'] = self.error_class([
                    'A password already exists for this website'])    
            if password1 != password2:
                self._errors['password2'] = self.error_class([
                    "Passwords don't match"])
            if Password.objects.exclude(pk=self.instance_pk).filter(password=password1, user=self.user).exists():
                self._errors['password1'] = self.error_class([
                    'This password is used on another website'])
            pass
         
        
        return self.cleaned_data
    
    def save(self):
        pass

    