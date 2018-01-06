from django.conf import settings
from django.db import models

# Create your models here.
class InternetUsage(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	start_time=models.DateTimeField()
	end_time=models.DateTimeField()
	volume=models.FloatField()

	def __str__(self):
		return self.user.phone_num