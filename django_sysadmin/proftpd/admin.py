from django_sysadmin.proftpd import models

from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django import forms
from django.conf import settings

from models import FTPUser

FTP_PASSWORD_HASHER = getattr(settings, "FTP_PASSWORD_HASHER", "sha1")
FTP_PASSWORD_SALT_FILE = getattr(settings, "FTP_PASSWORD_SALT_FILE", None)

assert(bool(FTP_PASSWORD_SALT_FILE) == True)



### actions

def setactive(modeladmin, request, queryset):
    queryset.update(active=True)
    setactive.short_description = "Set selected entries as active"

def setinactive(modeladmin, request, queryset):
    queryset.update(active=False)
    setinactive.short_description = "Set selected entries as NOT active"

## admin objects

class FTPUserForm(forms.ModelForm):
    class Meta:
        model = FTPUser
        widgets = {
            'password': forms.PasswordInput(render_value = True),
        }

    def clean_password(self):
        passwd = self.cleaned_data.get("password")
        old_pwd = self.instance.password
        if passwd != old_pwd:
            salt = open(FTP_PASSWORD_SALT_FILE).readline()
            passwd = make_password(passwd, salt, FTP_PASSWORD_HASHER)

        return passwd


class FTPUserAdmin(admin.ModelAdmin):
    form = FTPUserForm
    list_display = ('username', 'homedir', 'uid', 'gid', 'active', 'created', 'comment')
    list_filter = ('active', 'created' )
    search_fields = ['usernme', 'comment']
    actions = [setactive, setinactive]



admin.site.register(models.FTPUser, FTPUserAdmin)