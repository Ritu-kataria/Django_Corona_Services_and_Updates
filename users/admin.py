from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from .models import Profile

# Register your models here.
class CustomUserAdmin(BaseUserAdmin):


    list_display = ['email', 'name', 'phone', 'address', 'date_joined', 'last_login']
    search_fields = ('email', 'name')
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ('last_login', )
    fieldsets = ()

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields' : ('email', 'name', 'phone', 'address', 'file', 'password1', 'password2'),
        }),
    )
    
    ordering=('email',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)