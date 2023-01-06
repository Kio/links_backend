from celery import shared_task

from api.models import Link


@shared_task
def extract_links(link_id):
    link = Link.objects.get(id=link_id)
    link.contained_links = ["url_1", "url_2"]
    link.save()
