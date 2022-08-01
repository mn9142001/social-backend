from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, AbstractUser

# Create your models here.
def get_profile_pic_path(instance, filename):
    return 'profiles/{0}/pic/{1}'.format(instance.email, filename)


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields : dict):
        extra_fields.update({'is_superuser' : True, 'is_staff' : True})
        user = self.create_user(
            email=email,
            password=password, **extra_fields)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    gender_type = ((1, 'Male'), (2, 'Female'))
    first_name = models.CharField(('first name'), max_length=150, blank=True)
    last_name = models.CharField(('last name'), max_length=150, blank=True)
    email = models.EmailField(('email address'), blank=True, unique=True)
    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'),)
    chatted_with = models.ManyToManyField('self', blank=True)
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)
    bio = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(
        upload_to=get_profile_pic_path, null=True, blank=True,)
    following = models.ManyToManyField('self', blank=True)
    followers = models.ManyToManyField('self', blank=True)
    blocked =models.ManyToManyField('self', blank=True)
    birthday = models.DateField(null=True)

    objects = UserManager()


    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'


    def full_name(self):
        if self.first_name and self.last_name:

            return self.first_name + " " + self.last_name
        return self.email.strip().rsplit('@', 1)[0]

    def pic(self):
        return self.avatar if self.avatar else ""