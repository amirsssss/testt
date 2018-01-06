from django.conf import settings
from django.db import models


# Create your models here.
class call(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	otherside_no=models.CharField(max_length=20,default="23")
	call_in=models.BooleanField()
	start_time=models.DateTimeField()
	end_time=models.DateTimeField()

	def __str__(self):
		return self.user.phone_num