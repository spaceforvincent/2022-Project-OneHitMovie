from django import forms
from .models import Advertisement, AdvertisementComment

class AdvertisementCommentForm(forms.ModelForm):
    content = forms.CharField(
	    label='',
	    widget=forms.Textarea(
	        attrs={
	        'class': 'my-comment form-control',
	        'placeholder': '댓글을 남겨보세요.',
	        'rows' : 3,
	        'cols' : 50,
            'style' : 'width:800px;'
	        }
	    ),
	    error_messages = {
	    'required': '내용이 입력되지 않았습니다.'
	    }
    )
    class Meta:
        model = AdvertisementComment
        fields = ('content',) 


class AdvertisementForm(forms.ModelForm):

    title = forms.CharField(
        label = '제목',
        widget=forms.TextInput(
	        attrs={
	        'class': 'my-title form-control',
	        'placeholder': '제목을 작성해주세요',
			'style' : 'width:400px;'
	        }

    )
    )

    picture = forms.ImageField(
		label="제품 사진",
        required=False # 선택적으로 입력할 수 있음.
        ) 
    content = forms.CharField(
        label='제품 소개',
	    widget=forms.Textarea(
	        attrs={
	        'class': 'my-content form-control',
	        'placeholder': '제품을 소개해주세요.',
	        'rows' : 5,
	        'cols' : 50,
			'style' : 'width:400px; height:200px;'
	        }
	    ),
    )

    class Meta:
        model = Advertisement
        fields = ('title', 'content', 'picture')
