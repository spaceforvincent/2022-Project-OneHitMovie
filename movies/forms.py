from django import forms
from .models import Movie, MovieComment

class MovieCommentForm(forms.ModelForm):

    class Meta:
        model = MovieComment
        fields = ('content',)