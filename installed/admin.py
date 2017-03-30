from django.contrib import admin

# Register your models here.
from .models import SystemInstall, InstallRecord

admin.site.register(SystemInstall)
admin.site.register(InstallRecord)