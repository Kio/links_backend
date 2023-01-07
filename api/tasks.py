from asgiref.sync import async_to_sync
from celery import shared_task

from api.link_utils import extract_links_to_set
from api.models import Link


@shared_task
def extract_links(link_id):
    link = Link.objects.get(id=link_id)
    links = set()
    async_to_sync(extract_links_to_set)(link.url, links)
    link.contained_links = list(links)
    link.save()
