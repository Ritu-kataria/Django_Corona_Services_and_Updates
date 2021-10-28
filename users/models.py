from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#from .manager import CustomUserManager
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, address, phone, password=None):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        if not name:
            raise ValueError('The name must be set')
        if not address:
            raise ValueError('The address must be set')
        if not phone:
            raise ValueError('please provide a active phone number.')
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            address = address,
            phone = phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, name, phone, address, password=None):
       user = self.create_user(
           email=email,
           name=name,
           phone=phone,
           address=address,
           password=password
       )
       user.is_admin = True
       user.is_superuser = True
       user.is_staff = True
       user.save(using=self._db)
       return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField(max_length=80, verbose_name='Name', blank=True, unique=True)
    address = models.TextField(max_length=120)
    phone_regex = RegexValidator(regex = r'^[6789]\d{9}$', message= 'Invalid Phone number.')
    phone = models.CharField(validators=[phone_regex], max_length= 10, verbose_name='Phone', blank=True, unique=True)
    file = models.FileField(verbose_name='File')
    date_joined = models.DateTimeField(verbose_name='Date Joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Last Login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', 'address']
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True



class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    t_covid_beds = models.IntegerField(null=True, blank=True)
    v_covid_beds = models.IntegerField(null=True, blank=True)
    o_covid_beds = models.IntegerField(null=True, blank=True)
    t_ventilators = models.IntegerField(null=True, blank=True)
    v_ventilators = models.IntegerField(null=True, blank=True)
    o_ventilators = models.IntegerField(null=True, blank=True)
    t_icu_beds = models.IntegerField(null=True, blank=True)
    v_icu_beds = models.IntegerField(null=True, blank=True)
    o_icu_beds = models.IntegerField(null=True, blank=True)
    t_oxygen_beds = models.IntegerField(null=True, blank=True)
    v_oxygen_beds = models.IntegerField(null=True, blank=True)
    o_oxygen_beds = models.IntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, verbose_name='Last Updated', auto_now=True)
    # profile_image = models.ImageField(default='default-avatar.png', upload_to='users/', null=True, blank=True)

    def __str__(self):
        return '%s' % (self.user.email)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()