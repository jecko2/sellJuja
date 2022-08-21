from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from account.models import BaseUserModel


class BaseUserCreationForm(UserCreationForm):
    class Meta:
        model = BaseUserModel
        fields = ('email',)


class BaseUserChangeForm(UserChangeForm):
    class Meta:
        model = BaseUserModel
        fields = ('email',)
