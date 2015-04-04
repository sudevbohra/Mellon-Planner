from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.first_name + " " + self.last_name

"""
class Day(models.Model):
	name = models.CharField(max_length=10)

class Lecture(models.Model):
	days = models.ManyToManyField(Day, related_name = "lectures")
	time_start = models.TimeField(blank = True)
	time_end = models.TimeField(blank = True)
	recitations = models.ManyToManyField(Recitation, related_name = "lectures")


class Recitation(models.Model):
	days = models.ManyToManyField(Day, related_name = "recitations")
	time_start = models.TimeField(blank = True)
	time_end = models.TimeField(blank = True)

class Course(models.Model):
	course_id = models.IntegerField(max_length=7)
	name = models.CharField(max_length=100)
	lectures = models.ManyToManyField(Lecture, related_name = "course")
	units = models.IntegerField(max_length=2)
"""
