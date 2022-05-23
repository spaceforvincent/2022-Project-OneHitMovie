from django.shortcuts import get_list_or_404, render, redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash, get_user_model
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST,require_safe
from django.views.generic import FormView
from django.db.models import Q 
from movies.models import Movie, MovieComment


# Create your views here.

@require_http_methods(['GET','POST'])
def login(request) :
    if request.user.is_authenticated: #로그인된 사용자는 로그인 버튼 볼 필요 없다
        return redirect('movies:index')

    if request.method == 'POST': #로그인 처리
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'movies:index')

    else: #로그인 창
        form = AuthenticationForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/login.html', context)

@require_POST
def logout(request) : 
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('movies:index') 


def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        form.picture = request.FILES.get('picture')
        if form.is_valid():
            #회원 가입 후 자동으로 로그인 진행하기
            user = form.save(commit=False)
            user.picture=form.picture
            user.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form':form,
    }

    return render(request, 'accounts/signup.html', context)


@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request) #탈퇴하면서 해당 유저의 세션 데이터도 함께 지움
    return redirect('movies:index')


@login_required
@require_http_methods(['GET','POST'])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        form.picture = request.FILES.get('picture')
        if form.is_valid():
            if form.picture:
                user = form.save(commit=False)
                user.picture = form.picture
                user.save()
            else:
                form.save()
            return redirect('movies:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form' : form,
    }
    return render(request, 'accounts/update.html', context)

@login_required
@require_http_methods(['GET','POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) #비밀번호 바꿔도 세션 유지
            return redirect('movies:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form' : form,
    }
    return render(request, 'accounts/change_password.html', context)


def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    my_movies = person.like_movies.all()
    wish_movies = person.wish_movies.all()
    advertisements = person.advertisements.all()
    context = {
        'person' : person,
        'my_movies' : my_movies,
        'wish_movies' : wish_movies,
        'advertisements' : advertisements
    }
    return render(request, 'accounts/profile.html', context)

@require_POST
def follow(request, user_pk):
    # CODE HERE
    if request.user.is_authenticated:
        person = get_object_or_404(get_user_model(), pk=user_pk)
        if person != request.user:
            # if request.user in person.followers.all():
            if person.followers.filter(pk=request.user.pk).exists():
                person.followers.remove(request.user)
                followed = False
            else:
                person.followers.add(request.user)
                followed = True
        context = {
            'followed' : followed,
            'followings_count' : person.followings.count(),
            'followers_count' : person.followers.count(),
        }
        return JsonResponse(context)    
    return redirect('accounts:login')    

