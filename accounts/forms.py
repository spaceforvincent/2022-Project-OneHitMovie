from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

class CustomUserChangeForm(UserChangeForm):
    
    picture = forms.ImageField(
		label="프로필 사진",
        required=False # 선택적으로 입력할 수 있음.
        ) 
    
    bio = forms.CharField(
	    label='자기소개',
	    widget=forms.Textarea(
	        attrs={
	        'class': 'my-bio form-control',
	        'placeholder': '당신을 소개해주세요.',
	        'rows' : 5,
	        'cols' : 50,
	        }
	    ),
    )

    birthday = forms.DateField(
	label='생년월일',
	widget=forms.NumberInput(
		attrs={
		'type':'date',
        'class': 'my-birthday form-control',
		'placeholder': '생년월일을 입력해주세요',
		}
	),
	)

    blog_url = forms.CharField(
	label='대표 SNS',
	widget=forms.TextInput(
		attrs={
		'class': 'my-blog_url form-control',
		'placeholder': '대표 SNS 주소를 알려주세요',
		}
	),
	)
    class Meta:
        model = get_user_model() #user
        fields = ('email', 'bio', 'birthday', 'picture', 'blog_url')

class CustomUserCreationForm(UserCreationForm):
    
    picture = forms.ImageField(
		label="프로필 사진",
        required=False # 선택적으로 입력할 수 있음.
        ) 
    
    bio = forms.CharField(
	    label='자기소개',
	    widget=forms.Textarea(
	        attrs={
	        'class': 'my-bio form-control',
	        'placeholder': '당신을 소개해주세요.',
	        'rows' : 5,
	        'cols' : 50,
	        }
	    ),
    )

    birthday = forms.DateField(
	label='생년월일',
	widget=forms.NumberInput(
		attrs={
		'type':'date',
        'class': 'my-birthday form-control',
		'placeholder': '생년월일을 입력해주세요',
		}
	),
	)

    blog_url = forms.CharField(
	label='대표 SNS',
	widget=forms.TextInput(
		attrs={
		'class': 'my-blog_url form-control',
		'placeholder': '대표 SNS 주소를 알려주세요',
		}
	),
	)
    
    class Meta(UserCreationForm.Meta):
        model = get_user_model() #user
        fields = UserCreationForm.Meta.fields + ('email', 'bio', 'birthday', 'picture', 'blog_url')



class UserSearchForm(forms.Form):
    searched_user = forms.CharField(
		label='검색',
		widget=forms.TextInput(
		attrs={
		'class': 'my-search form-control',
		'size' : 30,
		'placeholder': '찾으시는 회원이 있으신가요?',
		}
		)
		)