from django.conf import settings
from django.db import models

# Create your models here.
class Messages(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	sms_in=models.BooleanField()
	sms_ph_no=models.CharField(max_length=20)
	length=models.IntegerField()
	time=models.DateTimeField()

	def __str__(self):
		return self.user.phone_num