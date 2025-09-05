from typing import Any
from django.db import models

from django.utils.translation import gettext_lazy as _

from commons.models import AbstractCommonModel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.


class UserManager(BaseUserManager):

    def _create_user(self, **kwargs: Any) -> 'User':
        user = self.model(**kwargs)
        user.set_password(kwargs.get("password"))
        user.save(using=self._db)
        return user

    def create_user(self, **kwargs: Any) -> 'User':
        kwargs["is_admin"] = False
        return self._create_user(**kwargs)

    def create_superuser(self, **kwargs: Any) -> 'User':
        kwargs["is_admin"] = True
        return self._create_user(**kwargs)


class User(AbstractCommonModel, AbstractBaseUser):
    first_name = models.CharField(
        verbose_name=_("First Name"), max_length=120, null=False, blank=False
    )
    last_name = models.CharField(
        verbose_name=_("Last Name"), max_length=120, null=False, blank=False
    )
    email = models.CharField(
        _("Email"), unique=True, max_length=120, db_index=True, null=False, blank=False
    )
    password = models.CharField(_("Password"), max_length=128, null=False, blank=False)
    profile_image_url = models.URLField(
        _("Profile Image Url"), max_length=1000, null=True
    )
    username = models.CharField(_("Username"), unique=True, max_length=120)
    is_active = models.BooleanField(
        _("Active"), default=True, help_text="Designates Whether A User Is Active"
    )
    is_admin = models.BooleanField(
        _("Admin"), default=False, help_text="Designates Whether A User Is An Admin"
    )
    USERNAME_FIELD = "email"
    objects = UserManager()

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_active and self.is_admin

    def has_module_perms(self, app_label):
        return self.is_active and self.is_admin

    def get_all_permissions(self, obj=None):
        return []

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta(AbstractCommonModel.Meta):
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Superuser(User):
    class Meta:
        verbose_name = _("Admin")
        verbose_name_plural = _("Admins")


class Preference(AbstractCommonModel):
    name = models.CharField(verbose_name=_("Preference"), unique=True, null=True, blank=False)

    def __str__(self):
        return f"{self.name}"


class Blogger(User):
    bio = models.TextField(max_length=500, blank=True)
    preferences = models.ForeignKey(verbose_name=_("Preferences"), to=Preference, on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = _("Blogger")
        verbose_name_plural = _("Bloggers")


class Follower(AbstractCommonModel):
    blogger = models.ForeignKey(
        to=Blogger,
        on_delete=models.CASCADE,
        related_name="followers",
        related_query_name="blogger_follower",
    )
    follower = models.ForeignKey(to=Blogger, on_delete=models.CASCADE)
