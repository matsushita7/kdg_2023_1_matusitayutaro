from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# class Tag(models.Model):
    

CATEGORY = (('text','テキスト'),('art','イラスト'),('handmade','ハンドメイド'),('movie','動画'),('game','ゲーム'))
class Coment(models.Model):
    text = models.TextField(max_length=100)
    images = models.ImageField(null=True,blank=True)
    category = models.CharField(
        default = 'テキスト',
        max_length = 10,
        choices = CATEGORY,
    )
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.text

class CommentFavoUser(models.Model):
    user_record = models.TextField(null=True,blank=True)
    commentID = models.IntegerField
    
class Reply(models.Model):
    text = models.TextField(max_length=100)
    images = models.ImageField(null=True,blank=True)
    comment_id = models.IntegerField(default=99)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class Profile(models.Model):
    text = models.TextField(max_length=100,null=True,blank=True,default='こんにちは')
    images = models.ImageField(null=True,blank=True,default='sns/icon.png')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    


class Review(models.Model):
    text = models.TextField(max_length=100)
    thumbnail = models.ImageField(null=True,blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

