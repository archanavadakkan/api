from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from rest_framework.authtoken.models import Token
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    tpl = 'email/passwordresetemail.html'
    email_plaintext_message = reset_password_token.key
    print(email_plaintext_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    context = {
        "email_plaintext_message": email_plaintext_message,
    }
    html_message = render_to_string(tpl, context)
    subject = "Reset Password!"
    send_mail(subject=subject, message='', from_email=from_email, recipient_list=[reset_password_token.user.email],
              html_message=html_message)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, password, email=None, phone=None, is_staff=False, is_admin=False, is_active=True):
        """
        Create and save a User with the given email and password.
        """
        if not password:
            raise ValueError('The Password must be set')

        if not (email or phone):
            raise ValueError('The Email or Phone must be set')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)  # change user password
        user.email = email
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):

        user = self.create_user(
            email=email,
            password=password,
            phone=None,
            is_staff=True,
            is_admin=True

        )

        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10, unique=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS = ['mobile']

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name = 'users'

    def _str_(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

