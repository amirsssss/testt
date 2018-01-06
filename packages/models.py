from django.db import models

# Create your models here.
class Package(models.Model):
	# name=models.CharField(max_length=20)
	operators_name=(('HA','Hamrah Avval'),('IC','Iran Cell'),('Sh','Shatel'),('RT','RighTel'),('Ta','Taliya'))
	company=models.CharField(max_length=2,choices=operators_name,blank=False)
	simchoice=(('e','etebari'),('d','daemi'))
	SIM_kind=models.CharField(max_length=1,choices=simchoice,blank=None)
	duration=models.DurationField()
	internet_vol_day=models.IntegerField()
	internet_vol_night=models.IntegerField()
	call_duration=models.DurationField()
	sms_count=models.IntegerField()
	price=models.IntegerField()

	def __str__(self):
		return self.operators_name