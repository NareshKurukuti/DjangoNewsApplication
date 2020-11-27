from __future__ import unicode_literals
from django.db import models

# Create your models here.


class Main(models.Model):

    name = models.CharField(max_length=30)
    about = models.TextField()
    abouttxt = models.TextField(default='')
    fb = models.CharField(default='-', max_length=30)
    tw = models.CharField(default='-', max_length=30)
    yt = models.CharField(default='-', max_length=30)
    tell = models.CharField(default='-', max_length=30)
    link = models.CharField(default='-', max_length=30)

    seo_txt = models.CharField(max_length=200)
    seo_keywords = models.TextField()

    set_name = models.CharField(default='-', max_length=30)

    picname = models.CharField(default="", max_length=250)
    picurl = models.CharField(default="", max_length=250)

    picnamefooter = models.CharField(default="", max_length=250)
    picurlfooter = models.CharField(default="", max_length=250)

    def __str__(self):
        return self.set_name+' | '+str(self.pk)
