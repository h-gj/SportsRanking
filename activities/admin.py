from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
# Register your models here.
from django.contrib.admin import ModelAdmin

from activities.models import Activity


class UserIdFilter(AutocompleteFilter):
    title = 'user_id' # display title
    field_name = 'user' # name of the foreign key field


class ActivitiesAdmin(ModelAdmin):
    autocomplete_fields = ['user']
    # search_fields = ('user__id',)
    list_filter = (UserIdFilter,)


admin.site.register(Activity, ActivitiesAdmin)
