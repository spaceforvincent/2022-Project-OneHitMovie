from django.contrib import admin
from .models import Movie, MovieComment
from .forms import MovieCommentForm

# 생략

@admin.register(MovieComment)
class MovieCommentAdmin(admin.ModelAdmin):
    form = MovieCommentForm

class MovieAdmin(admin.ModelAdmin):
    list_display = ['pk','title','overview','adult','released_date','vote_avg','poster_path']
admin.site.register(Movie, MovieAdmin)