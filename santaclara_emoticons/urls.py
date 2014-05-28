from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import ListView

from santaclara_emoticons.models import EmoticonsSet

urlpatterns =patterns('',
                      ( r'^emoticonssets/$',ListView.as_view(
                          model=EmoticonsSet,
                          context_object_name="emoticonsset_list")),
                      )

