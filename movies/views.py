from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .models import Movie, MovieComment
from .forms import MovieCommentForm
from django.db.models import Q
import datetime
from django.db.models import Avg

@require_safe
def index(request):
    this_month_movies = Movie.objects.filter(vote_avg__gte = 8.0, released_date__month=datetime.datetime.now().strftime ("%m"))[:20]
    if datetime.datetime.now().strftime ("%m")[0] == '0':
        this_month = datetime.datetime.now().strftime ("%m")[1]
    else:
        this_month = datetime.datetime.now().strftime ("%m")
    
    context = {
        'this_month_movies' : this_month_movies,
        'this_month' : this_month 
    }
    return render(request, 'movies/index.html', context)

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        User = get_user_model()        
        user_list = User.objects.filter(Q(username__icontains=searched))
        movie_list = Movie.objects.filter(Q(title__icontains=searched))
        context = {
            'searched': searched, 
            'user_list': user_list,
            'movie_list': movie_list,
        }
        return render(request, 'movies/search.html', context)
    else:
        return render(request, 'movies/search.html', {})

@require_safe
def detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    comment_form = MovieCommentForm()
    comments = movie.movie_comments.all()
    context = {
        'movie': movie,
        'comment_form' : comment_form,
        'comments' : comments,
    }
    return render(request, 'movies/detail.html', context)


@require_POST
def comments_create(request, pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=pk)
        comment_form = MovieCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False) #아직 데이터베이스에 저장되지 않은 인스턴스를 반환, 객체에 대한 사용자 지정처리를 수행할 때 유용
            comment.movie = movie #외래키 1
            comment.user = request.user #외래키 2
            comment.save()
        return redirect('movies:detail', movie.pk)
    return redirect('accounts:login')

@require_POST
def comments_delete(request, movie_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(MovieComment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('movies:detail', movie_pk)


@require_POST
def likes(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        user = request.user

        if movie.like_users.filter(pk=user.pk).exists():
            movie.like_users.remove(user)
            liked = False
        else:
            movie.like_users.add(user)
            liked = True
        context = {
            'liked' : liked,
            'count' : movie.like_users.count(),
        }

        return JsonResponse(context)
    return redirect('accounts:login')