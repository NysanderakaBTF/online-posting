from django.db import models

class Queue(models.Model):
    user_id = models.IntegerField(unique=True)
    post_ids = models.JSONField(default=list)