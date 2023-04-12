
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.http import HttpResponseBadRequest
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required

from .forms import UserForm

User = get_user_model()

def page_not_found(request, exception):
    """
    404 Page not found
    """
    return render(request, 'accounts/404.html', {})

@require_http_methods(['GET', 'POST'])
def signup(request):
    # login 되있으면 여기 오면 안됨!
    if request.user.is_authenticated:
        # 그대로 튕겨내기
        return redirect('blog:posting_index')
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()    # 새로 생성된 사용자
            login(request, user)  # 새로 생성된 사용자로 로그인(set cookie)
            return redirect('blog:posting_index')
    else:
        form = UserForm()
    return render(request, 'accounts/signup.html', {
        'form': form,
    })


@require_http_methods(['GET', 'POST'])
def signin(request):
    # login 되있으면 여기 오면 안됨!
    if request.user.is_authenticated:
        # 그대로 튕겨내기
        return redirect('blog:posting_index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        # ID/PW 가 맞다면,
        if form.is_valid():
            # AuthenticationForm은 용도가 다르기 때문에, .get_user() 메서드가 존재
            user = form.get_user()  # id/pw로 찾은 기존 사용자
            login(request, user)    # 기존 사용자로 로그인(set cookie)
            
            # 0. URL 에 ?와 &로 넘어오는 값들은 모두 request.GET 꾸러미에 담긴다.
            # 1. request.GET 은 dict
            # 2. dict의 get 메서드 떠올리기 
            # @login_required 로 튕겨서 올 경우 {'next': '/blog/create/'}.get('next') => '/blog/create/'
            # 그냥 접속한 경우 {}.get('next') => None
            # 3. or 은 1 or 2 or 3 / 0 or 1 or 2
            return redirect(request.GET.get('next') or 'blog:posting_index')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {
        'form': form,
    })


def signout(request):
    logout(request)
    return redirect('blog:posting_index')

