from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="home"),
    path("index", views.index),
    path("collect_data", views.collect_data, name="collect"),
    path("predict", views.predict, name="predict"),
    path("live_collect_data/", views.live_collect_data, name="live"),
]