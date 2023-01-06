from django.db import models
from django.contrib.postgres.fields import ArrayField


class Link(models.Model):
    url = models.URLField(max_length=1000)
    celery_task_id = models.CharField(max_length=1000, null=True, blank=True)
    contained_links = ArrayField(
        models.URLField(max_length=1000, blank=True),
        default=list
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
