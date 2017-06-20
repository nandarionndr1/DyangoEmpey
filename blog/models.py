from __future__ import unicode_literals
from django.utils.timezone import localtime, now
from django.db import models
from PIL import Image


# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, default="MARK")
    avatar = models.ImageField(upload_to='pics/', default="pics/default.jpeg")

    def __str__(self):
        return 'Post: {} {}'.format(self.first_name, self.last_name)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    date = models.DateTimeField(auto_created=True)
    title = models.CharField(max_length=100, default="")

    def __str__(self):
        return 'Post: {}'.format(self.author)
class Comment(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    cdate = models.DateTimeField(auto_created=True)

    def approve(self):
        self.approved_comment = True
        self.save()


    def __str__(self):
        return 'Comment {} #'.format(self.id)
