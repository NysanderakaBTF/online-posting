from django.db import models

class Template(models.Model):
    user_id = models.IntegerField()
    network_name = models.CharField(max_length=50)
    template_content = models.TextField()


class Block(models.Model):
    name = models.CharField(max_length=50)
    position = models.IntegerField()
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='blocks')