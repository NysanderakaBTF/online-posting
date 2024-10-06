from django.db import models

class Post(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    is_posted = models.BooleanField(default=False)
    text = models.TextField()
    user_id = models.BigIntegerField()

class Block(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='blocks')
