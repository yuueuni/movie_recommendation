from django.urls import path
from . import views

app_name = "movies"

urlpatterns = [
    path('', views.index, name="index"),

    path('movie_create/', views.movie_create, name='movie_create'),
    path('<int:movie_pk>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_pk>/movie_like/', views.movie_like, name='movie_like')
]
