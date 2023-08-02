# Register your models here.
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required

# from .models import Folder
from .models import Password
from .models import Setting
from .models import PasswordSharing, CompromisedSite


class PasswordAdmin(admin.ModelAdmin):
    list_display = ("website_name", "website_url", "username", "password", "user", "expiration_date", "sharing_token", "is_compromised", "is_active")
  
admin.site.register(Password, PasswordAdmin)


class SettingAdmin(admin.ModelAdmin):
    list_display = ("share_passwords", "expire_number", "expire_period", "user")
  
admin.site.register(Setting, SettingAdmin)


class PasswordSharingAdmin(admin.ModelAdmin):
    list_display = ("owner", "tenant", "password", "valid_until", "owner_authorize")
  
admin.site.register(PasswordSharing, PasswordSharingAdmin)

class CompromisedSiteAdmin(admin.ModelAdmin):
    list_display = ("website_name", "website_url")
  
admin.site.register(CompromisedSite, CompromisedSiteAdmin)



# # Ensure users go through the allauth workflow when logging into admin.
# admin.site.login = staff_member_required(admin.site.login, login_url='/accounts/login')
# # Run the standard admin set-up.
# admin.autodiscover()