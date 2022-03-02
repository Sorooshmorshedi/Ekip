from django.contrib import admin
from share.models import  Ekip, Share, Expense, Friends, MemberAmount, User
from django.contrib.auth.admin import UserAdmin
UserAdmin.fieldsets += (('profile pic', {'fields': ('profile_picture',)}),)
UserAdmin.fieldsets += (('status', {'fields': ('status',)}),)

admin.site.register(User,UserAdmin)
admin.site.register(Ekip)
admin.site.register(Share)
admin.site.register(Friends)
admin.site.register(Expense)
admin.site.register(MemberAmount)
