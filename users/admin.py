from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin
# from django.forms import forms
from django.forms import ModelForm

from users.models import User


class UserCreationForm(ModelForm):
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
