from django.db import models

# Create your models here.
class Question(models.Model):
    age = models.IntegerField()
    gender = models.IntegerField()
    style1 = models.IntegerField()
    style2 = models.IntegerField()
    style3 = models.IntegerField()
    style4 = models.IntegerField()
    style5 = models.IntegerField()
    style6 = models.IntegerField()
    style7 = models.IntegerField()
    style8 = models.IntegerField()
    MBTI = models.CharField(max_length=200)