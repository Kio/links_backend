import graphene
from django.shortcuts import get_object_or_404
from graphene_django import DjangoObjectType

from .models import *


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class CreateLinkMutation(graphene.Mutation):
    class Arguments:
        url = graphene.String(required=True)

    id = graphene.Int()

    def mutate(self, info, url):
        link = Link.objects.create(url=url)
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
