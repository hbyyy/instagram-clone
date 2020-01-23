import json
import os

import requests
from django.contrib.auth import login, logout, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from config.settings import BASE_DIR
from members.forms import LoginForm, SignupForm

# 장고 기본유저나 Custom
User = get_user_model()


def login_view(request):
    """

    :param request:
    :return:
    """

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            form.login(request)
            return redirect('posts:post_list')

        # username = request.POST['username']
        # password = request.POST['password']
        # user = authenticate(request, username=username, password=password)
        # if user is not None:
        #     login(request, user)
        #     return redirect('posts:post_list')
        # else:
        #     return redirect('members:login')
    else:
        form = LoginForm()

    login_base_url = 'https://nid.naver.com/oauth2.0/authorize'
    login_pattern = {
        'response_type': 'code',
        'client_id': 'ee6QeTwBsL1kM2f2_O7f',
        'redirect_uri': 'http://localhost:8000/members/naver-login/',
        'state': 'RANDOM_STATE'
    }
    login_url = '{base}?{params}'.format(
        base=login_base_url,
        params='&'.join(f'{key}={value}' for key, value in login_pattern.items())
    )
    print(login_url)
    context = {
        'form': form,
        'login_url': login_url
    }

    return render(request, 'members/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('members:login')


def naver_login(request):
    try:
        code = request.GET['code']
        state = request.GET['state']
    except KeyError:
        return HttpResponse('code나 state 값이 없습니다')

    with open(os.path.join(BASE_DIR, 'secret.json'), 'r') as secret_json:
        secret = json.load(secret_json)
    # 토큰 받아오기
    token_base_url = 'https://nid.naver.com/oauth2.0/token'
    url_params = {
        'grant_type': 'authorization_code',
        'client_id': 'ee6QeTwBsL1kM2f2_O7f',
        'client_secret': secret['NAVER_CLIENT_SECRET_KEY'],
        'redirect_uri': 'http://localhost:8000/members/naver-login/',
        'code': code,
        'state': state
    }

    token_url = '{base}?{params}'.format(
        base=token_base_url,
        params='&'.join(f'{key}={value}' for key, value in url_params.items())
    )

    response = requests.get(token_url)
    # access_token = json.loads(response.text)['access_token']
    access_token = response.json()['access_token']

    # 받아온 토큰 이용해서 unique_id를 받아온다
    header = {
        "Authorization": "Bearer " + access_token
    }
    profile_base_url = 'https://openapi.naver.com/v1/nid/me'
    response = requests.get(profile_base_url, headers=header)

    unique_id = response.json()['response']['id']

    user_check = User.objects.filter(username=f'n_{unique_id}').exists()

    if user_check is True:
        user = User.objects.get(username=f'n_{unique_id}')
    else:
        user = User.objects.create_user(username=f'n_{unique_id}')

    login(request, user)
    return redirect('posts:post_list')


def signup_view(request):
    """

    Template: index.html 을 복사해서 /members/signup.html에 사용
                action만 이쪽으로
    URL : /members/signup -> /  (변경)

    User에 name필드를 추가
        email
        username
        name
        password
    를 전달받아, 새로운 User를 생성한다,
    생성 시, User.objects.create_user() 메서드를 사용한다.

    이미 존재하는 username 또는 email을 입력한 경우,
    "이미 사용중인 username/email입니다" 라는 메시지를 HttpResponse로 돌려준다.

    생성에 성공하면 로그인 처리 후 (위의 login_view를 참조) posts:post-list로 redirection처리

    """
    if request.user.is_authenticated is True:
        return redirect('posts:post_list')

    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('signup')
    else:
        form = SignupForm()

        # return render(request, 'posts/post-list.html')

    context = {
        'form': form,
    }
    return render(request, 'members/signup.html', context)

    # username = request.POST['username']
    # email = request.POST['email']
    # name = request.POST['name']
    # password = request.POST['password']
    #
    # user_check = User.objects.filter(username=username).exists()
    # email_check = User.objects.filter(email=email).exists()
    # if user_check is True or email_check is True:
    #     return HttpResponse(f'이미 사용중인 username/email입니다')
    #
    # user = User.objects.create_user(username=username, password=password, email=email, name=name)
    # login(request, user)
    # return redirect('posts:post_list')
