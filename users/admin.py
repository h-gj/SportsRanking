from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin
# from django.forms import forms
from django.forms import ModelForm, forms, ChoiceField

from users.models import User


class UserCreationForm(ModelForm):
    # CHOICES = ((1, 'a'), (2, 'b'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['adname'] = ChoiceField(choices=self.get_choices())

    def get_adnames(self):
        adnames = User.objects.values_list('adname', flat=True).distinct()
        return adnames

    def get_choices(self):
        adnames = self.get_adnames()
        choices = [[adname, adname] for adname in adnames]
        return choices

    class Meta:
        model = User
        # fields = ('email',)
        fields = '__all__'

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdmin(ModelAdmin):
    search_fields = ['id']
    form = UserCreationForm


admin.site.register(User, UserAdmin)
