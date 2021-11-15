from django.db import models
from django_resized import ResizedImageField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User must have an email address.")
        if not username:
            raise ValueError("User must have a username.")

        user = self.model(
            email=self.normalize_email(email),
            username=username)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user


def get_profile_image_filepath(self, filename):
    return f'profile_images/{str(self.pk)}/{"profile_image.png"}'


def get_default_profile_image():
    return "rugurublogimages/defaultprofile.png"


class Account(AbstractBaseUser):
    email = models.EmailField(
        _('email address'), max_length=80, unique=True)
    username = models.CharField(max_length=32, unique=True)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name="late joined", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = ResizedImageField(size=[50, 50], crop=['middle', 'center'], quality=75, upload_to=get_profile_image_filepath,
                                      blank=True, null=True, verbose_name='Profile picture', default=get_default_profile_image)
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    objects = AccountManager()

    def get_profile_image_filename(self):
        """ get the name of uploaded image """
        return str(self.profile_image)[str(self.profile_image).index(f'profile_image/{self.pk}/'):]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
