from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class BaseUserModelManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError(_("Email must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **kwargs)
        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):

        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_active", True)

        if kwargs.get("is_superuser") is not True:
            raise ValueError(_("superuser must be set as is_superuser=True"))

        if kwargs.get("is_superuser") is not True:
            raise ValueError(_("superuser must be set as is_staff=True"))

        if kwargs.get("is_superuser") is not True:
            raise ValueError(_("superuser must be set as is_active=True"))

        return self.create_user(email, password, **kwargs)

