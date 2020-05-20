from django.urls import path

app_name = "moveis"

urlpatterns = [
    path('', views.index, name="index"),
]