from django import forms
from .models import MovieComment

class MovieCommentForm(forms.ModelForm):
    content = forms.CharField(
	    label='',
	    widget=forms.Textarea(
	        attrs={
	        'class': 'my-comment form-control',
	        'placeholder': '이 영화에 관한 평가를 남겨주세요.',
	        'rows' : 3,
	        'cols' : 50,
	        }
	    ),
	    error_messages = {
	    'required': '내용이 입력되지 않았습니다.'
	    }
    )
    STAR_CHOICES = [
        ('5',"★★★★★"),
        ('4',"★★★★"),
        ('3',"★★★"),
        ('2',"★★"),
        ('1',"★"),
        (None, '선택')
    ]
    rating = forms.ChoiceField(
        label='나의 별점',
        choices=STAR_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'my-score',
                'default' : None,
            },
        ),
        required=True
        
    )
    class Meta:
        model = MovieComment
        fields = ('rating','content',)