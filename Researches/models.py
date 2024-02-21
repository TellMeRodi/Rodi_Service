from django.db import models

# Create your models here.
class Question(models.Model):
    question = models.CharField(max_length=200)
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=200)

class Response(models.Model):
    session_key = models.CharField(max_length=40)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)