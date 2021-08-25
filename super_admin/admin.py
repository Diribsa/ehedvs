from django.contrib import admin
from .models import *
admin.site.site_header = "E-HEDVS Super Admin"
admin.site.site_title = "E-HEDVS Admin Area"
admin.site.index_title = "Welcome to the E-HEDVS admin area"

admin.site.register(University)
admin.site.register(ActivityLog)
