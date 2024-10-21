from django.contrib import admin
from .models import CustomUser,User,Company
# Register your models here.


admin.site.register(User)
admin.site.register(CustomUser)
admin.site.register(Company)
