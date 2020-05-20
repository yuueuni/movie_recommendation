from django.urls import path
from . import views

app_name = "moveis"

urlpatterns = [
    path('', views.index, name="index"),
]