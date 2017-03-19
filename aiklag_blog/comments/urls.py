from django.conf.urls import url
from .views import (
    comment_thread
    )


urlpatterns = [
    url(r'^(?P<id>\d+)/$', comment_thread, name="thread"),
    # url(r'^(?P<id>\d+)/delete/$', comment_delete),
]

