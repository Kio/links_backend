from django.urls import path
from graphene_django.views import GraphQLView

from api import views
from backend import settings

urlpatterns = [
	path('csrf/', views.csrf),
	path('api', GraphQLView.as_view(graphiql=settings.DEBUG)),
]
