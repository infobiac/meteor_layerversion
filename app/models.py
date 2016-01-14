from django.db import models

# Create your models here.
class User(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	prof_pic = models.CharField(max_length=300)
	first_log_in = models.BooleanField(default=True)
	email1 = models.CharField(max_length=100)
	idnumber = models.CharField(max_length=100, primary_key=True)
	def __str__(self):              # __unicode__ on Python 2
		return self.idnumber
	def full(self):
		return self.first_name + " " + self.last_name
	def first(self):
		return self.first_name
	def email(self):
		return self.email1
