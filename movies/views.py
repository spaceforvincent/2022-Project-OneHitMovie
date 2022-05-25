from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from sklearn.tree import plot_tree
from .models import Movie, MovieComment, Genre
from .forms import MovieCommentForm
from django.db.models import Q
import datetime
from django.core.paginator import Paginator
import pandas as pd
import numpy as np
import sqlite3
from sklearn.linear_model import Lasso
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform as sp_rand
import requests
from bs4 import BeautifulSoup

@require_safe
def index(request):
    #이달의 영화
    if datetime.datetime.now().strftime ("%m")[0] == '0':
        this_month = datetime.datetime.now().strftime ("%m")[1]
    else:
        this_month = datetime.datetime.now().strftime ("%m")
    this_month_movies = Movie.objects.filter(vote_avg__gte = 8.0, released_date__month=datetime.datetime.now().strftime ("%m"))[:20]
    
    #오늘의 영화
    if datetime.datetime.now().strftime ("%a") == 'Sun':
        today_message = '일요일이네요... 한 주를 차분하게 마무리 해봅시다!'
        today_movies = Movie.objects.filter(vote_avg__gte = 8.0, genres = '99') #다큐멘터리 추천
    elif datetime.datetime.now().strftime ("%a") == 'Mon':
        today_message = '극복하자 월요병! 희망찬 한 주의 시작!'
        today_movies = Movie.objects.filter(vote_avg__gte = 8.0, genres = '14')\
                    | Movie.objects.filter(vote_avg__gte = 8.0, genres = '10402')#판타지물, 음악영화 추천
    elif datetime.datetime.now().strftime ("%a") == 'Tue':
        today_message = '화요일엔 화끈한 영화로 달립시다!'
        today_movies = Movie.objects.filter(vote_avg__gte = 8.0, genres = '28') #액션 추천
    elif datetime.datetime.now().strftime ("%a") == 'Wed':
        today_message = '이제 겨우 수요일...? 시간 왜이렇게 안가죠. 당신의 시간을 뺏어드립니다.'
        today_movies = Movie.objects.filter(vote_avg__gte = 8.0, genres = '9648') \
                        | Movie.objects.filter(vote_avg__gte = 8.0, genres = '878')#미스테리물, SF물 추천
    elif datetime.datetime.now().strftime ("%a") == 'Thu':
        today_message = '아직 목요일이라니... 끔찍하네요. 끔찍한 공포영화 추천드립니다.'
        today_movies = Movie.objects.filter(vote_avg__gte = 8.0, genres = '27') #공포영화 추천
    elif datetime.datetime.now().strftime ("%a") == 'Fri':
        today_message = '기다리고 기다리던 불금이네요! 쌓여있던 스트레스 풀어봅시다~'
        today_movies = Movie.objects.filter(vote_avg__gte = 8.0, genres = '12') #어드벤처 추천
    elif datetime.datetime.now().strftime ("%a") == 'Sat':
        today_message = '여유로운 토요일~ TV시리즈물 어떠세요?'
        today_movies = Movie.objects.filter(vote_avg__gte = 8.0, genres = '10770') #TV Movies
    
    #지금의 영화
    if int(datetime.datetime.now().strftime("%H")) in range(0,7):
        now_message = "새벽감성... 잠이 안오시나요? 역사, 서부극 배달이요~"
        now_movies = Movie.objects.filter(vote_avg__gte = 8.0, genres = '36') \
                        | Movie.objects.filter(vote_avg__gte = 8.0, genres = '37')#역사, 서부극 영화 추천
    elif int(datetime.datetime.now().strftime("%H")) in range(8,12):
        now_message = "하루를 영화로 시작하려는 당신! 귀여운 애니메이션 어떠세요?"
        now_movies = Movie.objects.filter(vote_avg__gte = 8.0, genres = '16') #애니메이션 추천
    elif int(datetime.datetime.now().strftime("%H")) in range(12,18):
        now_message = "점심먹고 많이 졸리시죠? 당신의 잠을 깨워줄 영화들입니다."
        now_movies =  Movie.objects.filter(vote_avg__gte = 8.0, genres = '53') \
                    | Movie.objects.filter(vote_avg__gte = 8.0, genres ='10752')\
                     | Movie.objects.filter(vote_avg__gte = 8.0, genres = '80')#스릴러, 범죄, 전쟁 추천
    elif int(datetime.datetime.now().strftime("%H")) in range(18,24):
        now_message = "수고했어 오늘도~ 하루의 마무리를 위한 영화들입니다."
        now_movies = Movie.objects.filter(vote_avg__gte = 8.0, genres = '18') \
                    | Movie.objects.filter(vote_avg__gte = 8.0, genres = '35')\
                    | Movie.objects.filter(vote_avg__gte = 8.0, genres = '10749')\
                    | Movie.objects.filter(vote_avg__gte = 8.0, genres = '10751') #드라마, 코미디, 로맨스, 패밀리 추천

    # 웹스크롤링 ()
    url = 'https://www.kobis.or.kr/kobis/business/stat/online/onlineGenreStat.do?CSRFToken=sK9RAOafpyRvw9mdqZNNX2UWkSx3On9nXiL2MBvZ7Xo&loadEnd=0&searchType=search&sSearchYearFrom=2021&sSearchMonthFrom=08&sSearchYearTo=2022&sSearchMonthTo=02'
    response = requests.get(url).text
    data = BeautifulSoup(response, 'html.parser')
    tv_genre = data.select_one('#tbody_0 > tr:nth-child(1) > td.tal')
    change = {
        '액션' : 28,
        '애니메이션' : 16,
        '드라마' : 18,
        '범죄' : 80,
        '멜로/로맨스' : 10749,
        '코미디' : 35,
        '스릴러' : 53,
        '공포(호러)' : 27,
        '미스터리' : 9648,
        'SF' : 878,
        '어드벤처' : 12,
        '판타지' : 14,
        '사극' : 36,
        '전쟁' : 10752,
        '가족' : 10751,
        '다큐멘터리' : 99,
        '뮤지컬' : 10402,
        '서부극(웨스턴)' : 37,
    }
    # 추천 알고리즘

    recommend_movies = Movie.objects.filter(genres__in = list(change.values()))
    # print(tv_genre.text)
    # print(change[tv_genre.text])
    # for movie in movies:
    #     for genre in movie.genres.all():
    #         if change[tv_genre.text] == genre:
    #             recommend_movies.append(movie)
    #             break
    recommend_message = '요새 유행하고 있는 장르만 모아뒀어요.'


    
    if request.user.is_authenticated and request.user.movie_comments.all(): #로그인된 유저가 하나라도 평점 남긴게 있을 때 마이무비 가동
        con = sqlite3.connect("db.sqlite3")

        #movies
        movies = Movie.objects.all()
        
        df = []
        for movie in movies:
            movie_genres= movie.genres.all()
            
            genres = []
            for genre in movie_genres:
                genres.append(genre.name)
            df.append([movie.title, *genres])

        title = []
        for row in df:
            title.append(row.pop(0))
            
        title = pd.DataFrame(title).rename(columns={0:'title'})
        genres = df
        
        lst = []
        for i in range(len(genres)):
            lst.append('|'.join(genres[i]))

        lst = pd.DataFrame(lst).rename(columns={0:'genres'})
        
        df = pd.concat([title,lst], axis=1)

        movies = pd.read_sql("SELECT * FROM movies_movie", con)
        movies = movies[['id','title']]
        movies.rename(columns={'id' : 'movie_id'}, inplace = True)
        
        movies = pd.merge(movies,df, on='title')

        genres = movies['genres'].str.get_dummies(sep='|') #영화의 장르 여부를 1과 0으로 구분

        #rating
        ratings = pd.read_sql("SELECT movie_id,user_id,rating FROM movies_moviecomment", con)
        ratings = ratings.astype({'rating' : 'float'})
        ratings = ratings.merge(genres, how='inner', left_on='movie_id', right_index=True)
        user_rating = ratings[ratings['user_id'] == request.user.pk]
        genre_cols = genres.columns
        sunho_genre = pd.DataFrame(user_rating[genre_cols].sum().sort_values(ascending=False))[:5]
        sunho_genre = sunho_genre.rename(columns={0:'평가한 영화 수'})
        #lasso
        model = Lasso()
        param_grid = {'alpha' : sp_rand()}
        
        
        rsearch = RandomizedSearchCV(estimator= model, param_distributions=param_grid, n_iter=200, cv=20, random_state=17)
        rsearch.fit(user_rating[genre_cols], user_rating['rating']) #학습
        
        intercept = rsearch.best_estimator_.intercept_
        coef = rsearch.best_estimator_.coef_

        user_profile = pd.DataFrame([intercept, *coef], index=['intercept', *genre_cols], columns=['score'])
        predictions = rsearch.best_estimator_.predict(genres)
        genres['user_predictions'] = predictions

        # #user가 아직 안본 영화들만 추리고 거기서 추천해주기
        rating_predictions = genres[~genres.index.isin(user_rating['movie_id'])].sort_values('user_predictions', ascending=False)
        rating_predictions = rating_predictions.merge(movies[['movie_id','title']], left_index=True, right_on = 'movie_id')
        
        

        my_movies = Movie.objects.filter(id__in = list(rating_predictions['movie_id']))
        
        context = {
            'this_month' : this_month,
            'this_month_movies' : this_month_movies,
            'today' : datetime.datetime.now().strftime("%a"),
            'today_message' : today_message,
            'today_movies' : today_movies,
            'now_message' : now_message,
            'now_movies' : now_movies,
            'my_movies' : my_movies,
            'sunho_genres' : sunho_genre.to_html(),
            'recommend_movies' : recommend_movies,
            'recommend_message' : recommend_message
        }

    else:
        context = {
            'this_month' : this_month,
            'this_month_movies' : this_month_movies,
            'today' : datetime.datetime.now().strftime("%a"),
            'today_message' : today_message,
            'today_movies' : today_movies,
            'now_message' : now_message,
            'now_movies' : now_movies,
            'recommend_movies' : recommend_movies,
            'recommend_message' : recommend_message
        }

    return render(request, 'movies/index.html', context)

now_searched = ''
def usersearch(request):
    global now_searched
    User = get_user_model()  
    if request.method == 'POST':
        searched = request.POST['searched'] 
        now_searched = searched     
        
        user_list = User.objects.filter(Q(username__icontains=searched))
        
        user_paginator=Paginator(user_list,10)
        
        page_number = request.GET.get('page')
        user_page_obj = user_paginator.get_page(page_number)
        

        context = {
            'searched': searched, 
            'user_list' : user_list,
            'users': user_page_obj,
        }
        return render(request, 'movies/user_search.html', context)
    else:
        user_list = Movie.objects.filter(Q(title__icontains=now_searched))
        user_paginator=Paginator(user_list,10)
        page_number = request.GET.get('page')
        user_page_obj = user_paginator.get_page(page_number)
        context = {
            'searched': now_searched,
            'users': user_page_obj,
        }
        return render(request, 'movies/user_search.html', context)

def moviesearch(request):
    global now_searched
    if request.method == 'POST':
        searched = request.POST['searched']
        now_searched = searched
        movie_list = Movie.objects.filter(Q(title__icontains=searched))
        movie_paginator=Paginator(movie_list,10)
        page_number = request.GET.get('page')
        movie_page_obj = movie_paginator.get_page(page_number)

        context = {
            'searched': searched, 
            'movies': movie_page_obj,
        }
        return render(request, 'movies/movie_search.html', context)
    else:
        movie_list = Movie.objects.filter(Q(title__icontains=now_searched))
        movie_paginator=Paginator(movie_list,10)
        page_number = request.GET.get('page')
        movie_page_obj = movie_paginator.get_page(page_number)
        context = {
            'searched': now_searched,
            'movies': movie_page_obj,
        }
        return render(request, 'movies/movie_search.html', context)

@require_safe
def detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    comment_form = MovieCommentForm()
    comments = movie.movie_comments.all()
    advertisements = movie.advertisements.all()
    context = {
        'movie': movie,
        'comment_form' : comment_form,
        'comments' : comments,
        'advertisements' : advertisements,
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

@require_POST
def wish(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        user = request.user

        if movie.wish_users.filter(pk=user.pk).exists():
            movie.wish_users.remove(user)
            wished = False
        else:
            movie.wish_users.add(user)
            wished = True
        context = {
            'wished' : wished,
        }
        return JsonResponse(context)
    return redirect('accounts:login')


# def user_recommendation(request):
#     con = sqlite3.connect("db.sqlite3")

#     #movies
#     movies = Movie.objects.all()
    
#     df = []
#     for movie in movies:
#         movie_genres= movie.genres.all()
        
#         genres = []
#         for genre in movie_genres:
#             genres.append(genre.name)
#         df.append([movie.title, *genres])

#     title = []
#     for row in df:
#         title.append(row.pop(0))
        
#     title = pd.DataFrame(title).rename(columns={0:'title'})
#     genres = df
    
#     lst = []
#     for i in range(len(genres)):
#         lst.append('|'.join(genres[i]))

#     lst = pd.DataFrame(lst).rename(columns={0:'genres'})
    
#     df = pd.concat([title,lst], axis=1)

#     movies = pd.read_sql("SELECT * FROM movies_movie", con)
#     movies = movies[['id','title']]
#     movies.rename(columns={'id' : 'movie_id'}, inplace = True)
    
#     movies = pd.merge(movies,df, on='title')

#     genres = movies['genres'].str.get_dummies(sep='|') #영화의 장르 여부를 1과 0으로 구분

#     #rating
#     ratings = pd.read_sql("SELECT movie_id,user_id,rating FROM movies_moviecomment", con)
#     ratings = ratings.astype({'rating' : 'float'})
#     ratings = ratings.merge(genres, how='inner', left_on='movie_id', right_index=True)
#     user_rating = ratings[ratings['user_id'] == request.user.pk]
#     genre_cols = genres.columns
    
#     #lasso
#     model = Lasso()
#     param_grid = {'alpha' : sp_rand()}
#     rsearch = RandomizedSearchCV(estimator= model, param_distributions=param_grid, n_iter=200, cv=20, random_state=17)
#     rsearch.fit(user_rating[genre_cols], user_rating['rating']) #학습
    
#     intercept = rsearch.best_estimator_.intercept_
#     coef = rsearch.best_estimator_.coef_

#     user_profile = pd.DataFrame([intercept, *coef], index=['intercept', *genre_cols], columns=['score'])
#     predictions = rsearch.best_estimator_.predict(genres)
#     genres['user_predictions'] = predictions

#     #user가 아직 안본 영화들만 추리고 거기서 추천해주기
#     rating_predictions = genres[~genres.index.isin(user_rating['movie_id'])].sort_values('user_predictions', ascending=False)
#     rating_predictions = rating_predictions.merge(movies[['movie_id','title']], left_index=True, right_on = 'movie_id')
    
    

#     my_movies = pd.DataFrame(Movie.objects.filter(id__in = list(rating_predictions['movie_id'])))
    


#     context = {

#         'my_movies' : my_movies,

#     }

#     return render(request, 'movies/practice.html', context)
