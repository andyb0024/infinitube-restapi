from django.contrib import admin
from .models import Membership,Subscription,UserMembership
# Register your models here.
admin.site.register(Membership)
admin.site.register(Subscription)
admin.site.register(UserMembership)