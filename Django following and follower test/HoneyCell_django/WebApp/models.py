from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import User


class Followship(models.Model):
    following = models.ForeignKey(User, related_name="who_follows")
    follower = models.ForeignKey(User, related_name="who_is_followed")
    follow_datetime = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s follows %s at %s" %(self.following, self.follower, self.follow_datetime)