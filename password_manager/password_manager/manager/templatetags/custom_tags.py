from django import template
# from models import Setting

register = template.Library()


# def search_settings(value, arg):
#     if arg is None or arg=="":
#         return []
#     else:
#         value = Setting.objects.filter(user=arg)[0]
#         return value
    
# register.filter('search_settings', search_settings)