from django.contrib import admin

from electrovec.models import Category, Vehicle, Cart, V_Comment, UserDetails
admin.site.register(Vehicle)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(V_Comment)
admin.site.register(UserDetails)
# admin.site.register(tempclass)
