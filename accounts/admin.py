from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm,UserChangeForm

from .models import MyUser,Profile,ActivationCode,ActivationUrl


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('phone_num', 'is_admin')
    list_filter = ('phone_num','is_admin',)
    fieldsets = (
        (None, {'fields': ('phone_num', 'password')}),
        # ('Personal info', {'fields': ('name','family_name')}),
        ('Permissions', {'fields': ('is_staff','is_admin','is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_num', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('phone_num',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
admin.site.register(Profile)
admin.site.register(ActivationCode)
admin.site.register(ActivationUrl)

# admin.site.register(SetPasswordUrl)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
