from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save

from .utils import code_generator,urlcode_generator,pass_code_generator

PHONE_REGEX=".*9.........$"

class MyUserManager(BaseUserManager):
    def create_user(self, phone_num, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone_num:
            raise ValueError('Phone Number is not Valid!')

        user = self.model(
            phone_num=phone_num
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_num, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            phone_num,
            password=password,       
        )
        user.is_admin = True
        user.is_staff=True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    phone_num = models.CharField(
        verbose_name='phone number',
        max_length=16,
        unique=True,
        validators=[
            RegexValidator(
                    regex=PHONE_REGEX,
                    message="Please enter a valid Phone Number"
                )
        ]
    )

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'phone_num'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_num

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name=models.CharField(max_length=20,blank=False)
    family_name=models.CharField(max_length=30,blank=False)
    birthday=models.DateField(null=True)
    sexchoice=(('M','Male'),('F','Female'))
    gender=models.CharField(max_length=1,choices=sexchoice,blank=False)
    email = models.EmailField(verbose_name='email address',max_length=255,null=True)

    def __str__(self):
        return self.user.phone_num



# def post_save_activationurl_usermodel(sender,instance,created,*args,**kwargs):
#     if created:
#         print("Activation Url Created!")

# post_save.connect(post_save_activationurl_usermodel,sender=ActivationUrl)


class ActivationCode(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key=models.CharField(max_length=120)
    expired=models.BooleanField(default=False)

    def save(self,*args,**kwargs):
        self.key=code_generator()
        return super(ActivationCode,self).save(*args,**kwargs)

    def __str__(self):
        return self.user.phone_num

class ActivationUrl(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    urlkey=models.CharField(max_length=120)

    def save(self,*args,**kwargs):
        self.urlkey=urlcode_generator()
        return super(ActivationUrl,self).save(*args,**kwargs)

    def __str__(self):
        return self.user.phone_num

class SetPasswordUrl(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    passurlkey=models.CharField(max_length=120)

    def save(self,*args,**kwargs):
        self.passurlkey=pass_code_generator()
        return super(SetPasswordUrl,self).save(*args,**kwargs)

    def __str__(self):
        return self.user.phone_num


def post_save_activation_usermodel(sender,instance,created,*args,**kwargs):
    if created:
        print("Activation Created!")

def post_save_usermodel(sender,instance,created,*args,**kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
            ActivationCode.objects.create(user=instance)
            ActivationUrl.objects.create(user=instance)
            SetPasswordUrl.objects.create(user=instance)
        except:
            pass

post_save.connect(post_save_usermodel,sender=settings.AUTH_USER_MODEL)