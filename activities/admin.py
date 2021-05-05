from django.contrib import admin
# Register your models here.
from django.contrib.admin import ModelAdmin

from activities.models import Activity


class ActivitiesAdmin(ModelAdmin):
    autocomplete_fields = ['user']
    search_fields = ('user__id',)


admin.site.register(Activity, ActivitiesAdmin)
