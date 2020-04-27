from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

import api.models

admin.site.register(api.models.User, UserAdmin)
admin.site.register(api.models.Course, admin.ModelAdmin)
admin.site.register(api.models.UserCourseRelationship, admin.ModelAdmin)
admin.site.register(api.models.Grade, admin.ModelAdmin)
