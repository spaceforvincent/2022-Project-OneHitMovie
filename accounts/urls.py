from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('user_search/', views.user_search, name='user_search'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('password/', views.change_password, name='change_password'),
    path('user_search/<username>/', views.profile, name = 'profile'),
    path('<int:user_pk>/follow/',views.follow, name= 'follow'),
]