from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/comments/', views.comments_create, name='comments_create'), # GET / POST
    path('<int:movie_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'), # GET / POST
    path('<int:movie_pk>/likes/', views.likes, name='likes'),
    path('<int:movie_pk>/wish/', views.wish, name='wish'),
    path('usersearch/', views.usersearch, name='usersearch'),
    path('moviesearch/', views.moviesearch, name='moviesearch'),
    # path('practice/', views.user_recommendation, name='practice'),   
]