from django.contrib import admin

from .models import Profile

# Register your models here.
admin.site.register(Profile)


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ("user", "startDate", "endDate", "token", "trackerID")
    search_fields = ("trackerID", "user")
    list_filter = ("startDate", "endDate")
    raw_id_fields = ("user",)
