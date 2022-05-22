from django import forms
from .models import Advertisement, AdvertisementComment

class AdvertisementCommentForm(forms.ModelForm):

    class Meta:
        model = AdvertisementComment
        fields = ('content',) 


class AdvertisementForm(forms.ModelForm):

    picture = forms.ImageField(
		label="제품 사진",
        required=False # 선택적으로 입력할 수 있음.
        ) 

    class Meta:
        model = Advertisement
        fields = ('title', 'content', 'picture')
