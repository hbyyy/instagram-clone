from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.


def login_view(request):
    """

    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user.get_email_field_name())
        if user is not None:
            login(request, user)
            return redirect('posts:post_list')
        else:
            return redirect('members:login')

    else:
        return render(request, 'members/login.html')

def signup_view(request):
    """
    Template: intex.html 사용
                action만 이쪽으로
    URL : /members/signup

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
    :param request:
    :return:
    """
