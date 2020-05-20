from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from random import choice

from .models import Movie
from .forms import MovieForm

# Create your views here.
def index(request):
    movies = Movie.objects.order_by('-release_date')
    rec_movies = choice(movies)
    paginator = Paginator(movies, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'movies':movies,
        'page_obj': page_obj,
        'rec_movies': rec_movies,
    }

    return render(request, 'movies/index.html', context)

@login_required
def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.save()
            return redirect('movies:movie_detail', movie.pk)
    else:
        form = MovieForm()
    context = {
        'form': form
    }
    return render(request, 'movies/forms.html', context)

def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    context = {
        'movie': movie,
    }
    return render(request, 'movies/detail.html', context)



def movie_like(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)

    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        liked = False
    else:
        movie.like_users.add(user)
        liked = True
    context = {
        'liked': liked,
        'count': movie.like_users.count()
    }
    return JsonResponse(context)
