from django.forms import ModelForm, IntegerField, CharField, TextInput

from activities.models import Activity


class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        exclude = ('user', )

