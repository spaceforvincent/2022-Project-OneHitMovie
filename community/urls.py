from django.urls import path
from . import views

app_name='community'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/comments/', views.comments_create, name='comments_create'),
    path('<int:advertisement_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
    path('<int:advertisement_pk>', views.detail, name='detail'),
    path('<int:advertisement_pk>/likes/', views.likes, name='likes'), 
    path('create/<int:movie_pk>', views.create, name='create'),

]
