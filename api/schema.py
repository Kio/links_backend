import graphene
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.shortcuts import get_object_or_404
from django_celery_results.models import TaskResult
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from .models import *
from .tasks import extract_links


class LinkType(DjangoObjectType):
    status = graphene.String()

    def resolve_status(self, info, **kwargs):
        if not self.celery_task_id:
            return "NOT_EXISTED"
        try:
            return TaskResult.objects.get(task_id=self.celery_task_id).status
        except TaskResult.DoesNotExist:
            return "RUNNING"

    class Meta:
        model = Link


class CreateLinkMutation(graphene.Mutation):
    class Arguments:
        url = graphene.String(required=True)

    id = graphene.Int()

    def mutate(self, info, url: str):
        try:
            URLValidator()(url)
        except ValidationError:
            raise GraphQLError("Wrong url.")
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

    def resolve_link(self, info, id: int, **kwargs):
        return get_object_or_404(Link, id=id)


schema = graphene.Schema(query=Query, mutation=Mutation)
