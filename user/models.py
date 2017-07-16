from django.db import models


# 继承
class User(models.Model):
    username = models.CharField(max_length=30, unique=True, blank=False, null=False)
    password = models.CharField(max_length=30, blank=False)
    register_time = models.DateTimeField()

    def __unicode__(self):
        return self.username
