from django.db import models


class Link(models.Model):
    url = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
