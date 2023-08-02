# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

from django.urls import path, reverse

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm

from pprint import pprint
from django.contrib.auth import get_user_model

from django.shortcuts import redirect
from .models import Password, Setting, PasswordSharing, CompromisedSite

from .forms import AddPasswordForm

from qr_code.qrcode.utils import QRCodeOptions

import secrets, hashlib

from datetime import date, datetime, timedelta

from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage

# def accueil(request):
#     return HttpResponse("Bonjour à tous.")

#######################  REDIRECT TO DASHBOARD  #######################    


def redirect_to_login(request):
    return redirect('account_login')

@login_required
def dashboard(request):

    user = request.user
    context = {
        'passwords_count' :  Password.objects.filter(user=user).count(),
        'passwords_compromised_count' : Password.objects.filter(user=user, is_compromised=True).count(),
        'passwords_inactive_count' : Password.objects.filter(user=user, is_active=False).count(),
        'passwords_sharing_number' : PasswordSharing.objects.filter(owner=user).count()
    }

    return render(request, "content-pages/dashboard.html", context)

#######################  REDIRECT TO PASSWORDS  ####################### 
@login_required       
def passwords(request):

    c_sites = CompromisedSite.objects.all()
    user = request.user
    passwords = Password.objects.filter(user=user)
    settings = Setting.objects.filter(user=user).first()

    csites_array = []

    for site in c_sites:
        csites_array.append(site.website_url)
    
    for password in passwords:
        if password.expiration_date is not None and password.expiration_date <= date.today():
            password.is_active = False
            password.save()
        else:
            password.is_active = True
            password.save()

        if password.website_url in csites_array:
            password.is_compromised = True
            password.save()
        else:
            password.is_compromised = False
            password.save()
            pass
        
    # return HttpResponse(csites_array) 

    return render(request, "content-pages/passwords/passwords.html", {'passwords': passwords, 'settings': settings})

#######################  REDIRECT TO SHARED PASSWORDS  ####################### 
@login_required
def shared_passwords(request):
    user = request.user
    # shared_passwords = PasswordSharing.objects.filter(tenant=user, owner_authorize=True).exclude(valid_until=None)
    shared_passwords = PasswordSharing.objects.filter(tenant=user, owner_authorize=True)
    # settings = Setting.objects.filter(user=user).first()
    return render(request, "content-pages/passwords/shared-passwords.html", {'passwords': shared_passwords})


#######################  REDIRECT TO SHARING PANEL  ####################### 
@login_required
def my_shares(request):
    user = request.user
    my_shares = PasswordSharing.objects.filter(owner=user)
    # settings = Setting.objects.filter(user=user).first()
    return render(request, "content-pages/passwords/sharing-panel.html", {'shares': my_shares})

#######################  CHANGE SHARING STATE (AUTHORIZE OR NOT)  ####################### 
@login_required
def share_state(request, pk):
    share = PasswordSharing.objects.filter(pk=pk).first()
    if share.owner == request.user:
        share.owner_authorize = not share.owner_authorize
        share.save()
        messages.success(request, 'Changes saved!')
    else:
        messages.warning(request, 'You are not allowed to perform this action!')

    return redirect('sharing-panel')

#######################  DELETE SHARING  ####################### 
@login_required
def delete_share(request, pk):
    share = PasswordSharing.objects.filter(pk=pk).first()
    if share.owner == request.user:
        share.delete()
        messages.success(request, 'Share deleted!')
    else:
        messages.warning(request, 'You are not allowed to perform this action!')

    return redirect('sharing-panel')



#######################  ADD PASSWORD  ####################### 
@login_required       
def add_password(request):
    if request.method == 'POST':
        form = AddPasswordForm(request.POST, user=request.user, instance_pk=None)
        if form.is_valid():

            settings = Setting.objects.filter(user=request.user).first()

            if settings and settings.expire_number != 0 and settings.expire_period > 1:
                if settings.expire_period == 2:
                    expiration_date = date.today() + timedelta(days=settings.expire_number)
                elif settings.expire_period == 3:
                    expiration_date = date.today() + timedelta(days=30*settings.expire_number)
                elif settings.expire_period == 4:
                    expiration_date = date.today() + timedelta(days=360*settings.expire_number)
                else:
                    # expiration_date = ""
                    expiration_date = None
            else:
                # expiration_date = ""
                expiration_date = None

            password_data = {
                'website_name': request.POST['website_name'],
                'website_url': request.POST['website_url'],
                'username': request.POST['username'],
                'password': request.POST['password1'],
                'expiration_date' : expiration_date,
                'sharing_token' : hashlib.sha256(secrets.token_hex(8).encode('utf-8')).hexdigest(),
                'user_id': request.user.id
            }
            password = Password(**password_data)
            password.save()

            messages.success(request, 'Password created successfully!')
            return redirect('passwords')
        # else:
        #     messages.warning(request, 'Oops! Something went wrong.')
        #     return redirect(request.META.get('HTTP_REFERER')) 
    else:
        form = AddPasswordForm(user=request.user, instance_pk=None)
    return render(request, "content-pages/passwords/add-password.html", {'form': form})


#######################  UPDATE PASSWORD  ####################### 
@login_required       
def update_password(request, pk):
    password = get_object_or_404(Password, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AddPasswordForm(request.POST, user=request.user, instance_pk=pk)
        if form.is_valid():

            settings = Setting.objects.filter(user=request.user).first()

            if settings and settings.expire_number != 0 and settings.expire_period > 1:
                if settings.expire_period == 2:
                    expiration_date = password.created_at + timedelta(days=settings.expire_number)
                elif settings.expire_period == 3:
                    expiration_date = password.created_at + timedelta(days=30*settings.expire_number)
                elif settings.expire_period == 4:
                    expiration_date = password.created_at + timedelta(days=360*settings.expire_number)
                else:
                    expiration_date = ""
            else:
                expiration_date = ""

            password = password
            password.website_name = request.POST['website_name']
            password.website_url = request.POST['website_url']
            password.username = request.POST['username']
            password.password = request.POST['password1']
            password.expiration_date = expiration_date
            password.sharing_token = hashlib.sha256(secrets.token_hex(8).encode('utf-8')).hexdigest() if password.sharing_token is None else password.sharing_token
            password.save()

            messages.success(request, password.website_name + ' Password updated successfully!')
            return redirect('passwords')
        # else:
        #     messages.warning(request, 'Oops! Something went wrong.')
        #     return redirect(request.META.get('HTTP_REFERER')) 
    else:
        form = AddPasswordForm(user=request.user, instance=password, instance_pk=pk, initial={'password1': password.password, 'password2': password.password})
    return render(request, "content-pages/passwords/edit-password.html", {'form': form}) 


#######################  CONFIRM SHARING  #######################
@login_required
def access_password_sharing(request, token, valid_until):

    password = Password.objects.filter(sharing_token=token).first()

    if PasswordSharing.objects.filter(owner=password.user, tenant=request.user, password=password).exists():
        messages.warning(request, 'This link has already been shared with you')
    else:
        if password and password.user != request.user:
            PasswordSharing.objects.create(
                owner = password.user,
                tenant = request.user,
                password = password,
                valid_until = None if valid_until == "undefined" else valid_until
            )
            messages.success(request, 'Password shared with you successfully!')
        elif password.user == request.user:
            messages.warning(request, 'You are the owner of this password!')
        else:
            messages.warning(request, 'Something went wrong!')
        
        return redirect('passwords')
    
#######################  DELETE PASSWORD  #######################
@login_required       
def delete_password(request, pk):
    password = get_object_or_404(Password, pk=pk)
    if request.method == 'POST':
        password.delete()
        messages.success(request, 'Password deleted successfully!')
        return redirect('passwords')

    return render(request, 'passwords.html', {})


#######################  SAVE OTHER SETTINGS FOR APP  #######################
@login_required
def additional_settings(request):
    user = request.user 
    if request.method == "POST":
        if int(request.POST['expire_number']) < 1:
            return HttpResponse(f'<div class="alert alert-danger alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>Number must be greater than 0 !</div>')
        settings = Setting.objects.filter(user=user).first()
        share_passwords = request.POST.get("share_passwords", None)
        if settings is not None:
            settings.share_passwords = True if share_passwords in ['on', 'True'] else False
            settings.expire_number = abs(int(request.POST['expire_number']))
            settings.expire_period = request.POST['expire_period']
            settings.save()
            return HttpResponse(f'<div class="alert alert-success alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>Changes saved !</div>')
        else:
            Setting.objects.create(
                share_passwords = True if share_passwords in ['on', 'True'] else False,
                expire_number = abs(int(request.POST['expire_number'])),
                expire_period = request.POST['expire_period'],
                user = user
            )
            return HttpResponse(f'<div class="alert alert-success alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>Changes Saved !</div>')
    else:
        settings = Setting.objects.filter(user=user).first()
        context = dict(
            settings = settings
        )
        return render(request, 'content-pages/other-settings/add-settings.html', context=context)


#######################  SHOW QR CODE WITHOUT VALID_UNTIL  #######################
@login_required 
def show_qr_image(request, pk):
    password = get_object_or_404(Password, pk=pk, user=request.user)

    context = dict(
        my_options = QRCodeOptions(size='13', border=8, error_correction='L'),
        password = password,
        valid_until = "",
        qr_text = request.build_absolute_uri(reverse('password-share-access', kwargs={'token': password.sharing_token, 'valid_until': "undefined"}))
    )
    return render(request, 'content-pages/passwords/share-password.html', context=context)


#######################  SHOW QR CODE WITHVALID_UNTIL  #######################
@login_required 
def show_qr_image2(request, pk):
    
    pk = pk

    valid_until = datetime.strptime(request.POST['valid_until'], '%Y-%m-%d')

    password = get_object_or_404(Password, pk=pk, user=request.user) 

    if valid_until.date() <= date.today():
        messages.warning(request, 'Validity date must be greater than today date!')
        context = dict(
            my_options = QRCodeOptions(size='13', border=8, error_correction='L'),
            password = password,
            valid_until = request.POST['valid_until'],
            qr_text = request.build_absolute_uri(reverse('password-share-access', kwargs={'token': password.sharing_token, 'valid_until': 'undefined'}))
        )
    else:
        context = dict(
            my_options = QRCodeOptions(size='13', border=8, error_correction='L'),
            password = password,
            valid_until = request.POST['valid_until'],
            qr_text = request.build_absolute_uri(reverse('password-share-access', kwargs={'token': password.sharing_token, 'valid_until': request.POST['valid_until']}))
        )

    return render(request, 'content-pages/passwords/share-password.html', context=context)


#######################  SHOW QR CODE WITHVALID_UNTIL  #######################
@login_required
def sendmail(request):


    User = get_user_model()
    password = get_object_or_404(Password, pk=request.POST['password_pk'])

    if User.objects.filter(email=request.POST['email']).exists():
        user = get_object_or_404(User, email=request.POST['email'])
        ctx = {
            'user' : user,
            'link' : request.POST['qr_text'],
            'password' : password
        }

        message = get_template('emails/share_link.html').render(ctx)
            

        msg = EmailMessage(
            "Password Sharing Link",
            message,
            'notifications@password-manager.com',
            [request.POST['email']],
        )
        msg.content_subtype = "html" # Main content is now text/html
        msg.send()

        messages.success(request, 'Mail sent successfully to user !')

    else:
        messages.warning(request, 'Something went wrong')

    return redirect('passwords')



#######################  EDIT PROFILE  #######################
def edit_profile(request):
    if request.method == "POST":

        User = get_user_model()

        users = User.objects.exclude(pk=request.user.id).filter(username=request.POST['username']).exists()
        users2 = User.objects.exclude(pk=request.user.id).filter(email=request.POST['email']).exists()

        if users:
            return HttpResponse(f'<div class="alert alert-danger alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>Username was already taken by someone else !</div>')
        elif users2:
            return HttpResponse(f'<div class="alert alert-danger alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>Email address was already taken by someone else !</div>')


        user = request.user
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        return HttpResponse(f'<div class="alert alert-success alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>Changes saved !</div>')
    else:
        pass

#######################  CHANGE PASSWORD  #######################
def edit_password(request):
    user = request.user 
    if request.method == "POST":
        if not user.check_password(request.POST['cpassword']):
            return HttpResponse(f'<div class="alert alert-danger alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>Wrong Password !</div>')
        else:
            if request.POST['npassword'] != request.POST['npassword2']:
                return HttpResponse(f'<div class="alert alert-danger alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>Passwords entered are not the same</div>')
            else:   
                user.set_password(request.POST['npassword'])  # replace with your real password
                user.save()
                return HttpResponse(f'<div class="alert alert-success alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>Password updated !</div>')
    else:
        pass

#######################  REGISTER ROUTE (NO USE)  #######################
def register(request):
    if request.method == 'GET':
        form  = RegisterForm()
        context = {'form': form}
        return render(request, 'registration/register.html', context)
    if request.method == 'POST':
        form  = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('dashboard')
        else:
            print('Form is not valid')
            messages.error(request, 'Error Processing Your Request')
            context = {'form': form}
            return render(request, 'registration/register.html', context)
            return render(request, 'registration/register.html', {})