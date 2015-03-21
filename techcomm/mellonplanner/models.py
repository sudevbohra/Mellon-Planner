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
