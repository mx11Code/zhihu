from django.db import models

from zhihu.models import BaseModel
from user.models import User


#
# # Create your models here.

class Question(BaseModel):
    title = models.CharField('title', max_length=30)
    content = models.CharField('content', max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name="follower")
    viewed_numbers = models.BigIntegerField(default=0)


class Answer(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    like = models.IntegerField(default=0)
    viewed_numbers = models.IntegerField(default=0)


class Comment(BaseModel):
    content = models.CharField("content", max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Tag(BaseModel):
    content = models.CharField("content", max_length=30)
    question = models.ManyToManyField(Question)
