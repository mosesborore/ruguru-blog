from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


from versatileimagefield.fields import  VersatileImageField
from versatileimagefield.image_warmer import VersatileImageFieldWarmer


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
    profile_image = VersatileImageField(
        upload_to="user-profile-images", height_field='height', width_field='width',
        blank=True, null=True,
        verbose_name='Profile picture',
        default=get_default_profile_image
        )
    height = models.PositiveIntegerField(
        'Profile Image Height',
        blank=True,
        null=True
    )
    width = models.PositiveIntegerField(
        'Profile Image Width',
        blank=True,
        null=True
    )
    
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']
    objects = AccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

@receiver(models.signals.post_save, sender=Account)
def warm_Account_profile_images(sender, instance, **kwargs):
    profile_img_warmer = VersatileImageFieldWarmer(
        instance_or_queryset=instance,
        rendition_key_set="user_profile",
        image_attr="profile_image"
    )
    
    num_created, failed_to_create = profile_img_warmer.warm()
    if num_created:
        print("successful image warmer created")
    if failed_to_create:
        print("unsuccessful image warmer")
