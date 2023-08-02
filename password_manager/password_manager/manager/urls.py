# MES ROUTES

from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

from django.urls import path, re_path
from . import views
from django.conf.urls import include


urlpatterns=[
    path('', views.redirect_to_login),
    path('accounts/two-factor/', include('allauth_2fa.urls')),
    path('accounts/', include('allauth.urls')),
    # DASHBOARD ROUTES
    path('dashboard/', views.dashboard, name='dashboard'),
    # PASSWORD ROUTES
    path('add-password/', views.add_password, name='add-password'),
    path('passwords/<int:pk>/delete/', views.delete_password, name='delete-password'),
    path('passwords/<int:pk>/update/', views.update_password, name='update-password'),
    path('passwords/<int:pk>/share/', views.show_qr_image, name='share-password'),
    path('passwords/<int:pk>/share-with-date/', views.show_qr_image2, name='share-password-with-date'),
    path('passwords/', views.passwords, name='passwords'),
    path('shared-passwords/', views.shared_passwords, name='shared-passwords'),
    path('sharing-panel/', views.my_shares, name='sharing-panel'),
    path('sharing-state/<int:pk>/change', views.share_state, name='sharing-state'),
    path('sharing-delete/<int:pk>/delete', views.delete_share, name='sharing-delete'),
    path('send-mail/', views.sendmail, name='send-mail'),
    path('password-share-access/token_<str:token>/validity_<str:valid_until>/', views.access_password_sharing, name='password-share-access'),
    # re_path(
    #     r"^password-share-access/token/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$",
    #     views.access_password_sharing,
    #     name="password-share-access",
    # ),

    # ADDITIONAL SETTINGS
    path('other-settings/', views.additional_settings, name='other-settings'),

    # PROFILES ROUTES
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('edit-password/', views.edit_password, name='edit-password'),
]