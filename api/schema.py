import graphene
from django.shortcuts import get_object_or_404
from django_celery_results.models import TaskResult
from graphene_django import DjangoObjectType

from .models import *
from .tasks import extract_links


class LinkType(DjangoObjectType):
    status = graphene.String()

    def resolve_status(self, info, **kwargs):
        if not self.celery_task_id:
            return "NOT_EXISTED"
        return TaskResult.objects.get(task_id=self.celery_task_id).status

    class Meta:
        model = Link


class CreateLinkMutation(graphene.Mutation):
    class Arguments:
        url = graphene.String(required=True)

    id = graphene.Int()

    def mutate(self, info, url):
        link = Link.objects.create(url=url)
        link.celery_task_id = extract_links.delay(link.id)
        link.save()
        return CreateLinkMutation(id=link.id)


class Mutation(graphene.ObjectType):
    create_link = CreateLinkMutation.Field()


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)
    link = graphene.Field(LinkType, id=graphene.Int())

    def resolve_links(self, info, **kwargs):
        return Link.objects.all().order_by("-id")

    def resolve_link(self, info, id, **kwargs):
        return get_object_or_404(Link, id=id)


schema = graphene.Schema(query=Query, mutation=Mutation)
