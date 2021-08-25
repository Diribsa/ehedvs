from django.contrib import admin
from.models import User, RegistrarAdmin, RegistrarStaff


admin.site.register(User)
admin.site.register(RegistrarStaff)
admin.site.register(RegistrarAdmin)
