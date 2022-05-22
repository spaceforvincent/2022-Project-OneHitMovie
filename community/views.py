from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from community.models import Advertisement, AdvertisementComment
from community.forms import AdvertisementCommentForm
from .forms import AdvertisementCommentForm, AdvertisementForm
from django.views.decorators.http import require_POST, require_safe, require_http_methods
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Movie
# Create your views here.
@require_safe
def index(request):
    advertisements = Advertisement.objects.order_by('-pk')
    context = {
        'advertisements' : advertisements,
    }
    return render(request, 'community/index.html', context)

@require_safe
def detail(request, advertisement_pk):
    advertisement = get_object_or_404(Advertisement, pk=advertisement_pk)
    comment_form = AdvertisementCommentForm()
    comments = advertisement.advertisement_comments.all()
    context = {
        'advertisement' : advertisement,
        'comment_form' : comment_form,
        'comments' : comments
    }
    return render(request, 'community/detail.html', context)


@require_POST
def comments_create(request, pk):
    if request.user.is_authenticated:
        advertisement = get_object_or_404(Advertisement, pk=pk)
        comment_form = AdvertisementCommentForm(request.POST)
        if comment_form.is_valid():
            Comment = comment_form.save(commit=False) #아직 데이터베이스에 저장되지 않은 인스턴스를 반환, 객체에 대한 사용자 지정처리를 수행할 때 유용
            Comment.advertisement = advertisement #외래키 1
            Comment.user = request.user #외래키 2
            Comment.save()
        return redirect('community:detail', advertisement.pk)
    return redirect('accounts:login')

@require_POST
def comments_delete(request, article_pk, Comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(AdvertisementComment, pk=Comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('community:detail', article_pk)


@require_POST
def likes(request, advertisement_pk):
    if request.user.is_authenticated:
        advertisement = get_object_or_404(Advertisement, pk=advertisement_pk)
        user = request.user

        if advertisement.like_users.filter(pk=user.pk).exists():
            advertisement.like_users.remove(user)
            liked = False
        else:
            advertisement.like_users.add(user)
            liked = True
        context = {
            'liked' : liked,
            'count' : advertisement.like_users.count(),
        }

        return JsonResponse(context)
    return redirect('accounts:login')

@login_required
@require_http_methods(['GET', 'POST'])
def create(request, movie_pk):
    
    movie = get_object_or_404(Movie, pk=movie_pk)
    
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        form.picture = request.FILES.get('picture')
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.user = request.user
            advertisement.movie = movie
            advertisement.picture = form.picture
            advertisement.save()
            return redirect('community:detail', advertisement.pk)
    else:
        form = AdvertisementForm()
    context = {
        'form': form,
    }
    return render(request, 'community/create.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    if request.user == advertisement.user:
        if request.method == 'POST':
            form = AdvertisementForm(request.POST, instance=advertisement)
            form.picture = request.FILES.get('picture')
            if form.is_valid():
                if form.picture:
                    advertisement = form.save(commit=False)
                    advertisement.picture = form.picture
                    advertisement.save()
                else:
                    form.save()
                return redirect('community:detail', advertisement.pk)
        else:
            form = AdvertisementForm(instance=advertisement)
    else:
        return redirect('community:index')
    context = {
        'advertisement': advertisement, 
        'form': form,
    }
    return render(request, 'community/update.html', context)

@require_POST
def delete(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    if request.user.is_authenticated:
        if request.user == advertisement.user:
            advertisement.delete()
    return redirect('community:index')