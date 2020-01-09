from django.contrib.auth import login, logout, get_user_model
from django.shortcuts import render, redirect

# Create your views here.
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

    context = {
        'form': form,
    }

    return render(request, 'members/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('members:login')


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
