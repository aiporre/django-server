from django.db import models
from django.utils import timezone
# Create your models here.

class Cat(models.Model):
    cat_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('creation_date')
    def __str__(self):
        return self.cat_name
    def was_published_recently(self):
        return self.pub_date>=timezone.now()-timezone.timedelta(days=1)

class Details(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    description = models.CharField(default='', blank=True, max_length=200)
    age = models.IntegerField(default=1)
    likes = models.IntegerField(default=0)
    picturelink = models.CharField(default='static/images/catface150X150.png',max_length=200)
    def __str__(self):
        return self.description
