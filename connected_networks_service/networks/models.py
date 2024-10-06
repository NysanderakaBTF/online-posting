from django.db import models

class ConnectedNetwork(models.Model):
    user_id = models.IntegerField()
    network_name = models.CharField(max_length=50)
    auth_key = models.CharField(max_length=512)
    post_url = models.CharField(max_length=512)
