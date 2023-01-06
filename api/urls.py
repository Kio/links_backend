from django.urls import path
from graphene_django.views import GraphQLView

from backend import settings

urlpatterns = [
	path('api', GraphQLView.as_view(graphiql=settings.DEBUG)),
]
