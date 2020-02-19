from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from posts.forms import PostCreateForm, CommentCreateForm
from posts.models import Post, PostLike, PostComment


def post_list(request, tag=None):
    # 1. 로그인 완료 후 이 페이지로 이동하도록 함
    # 2. index에 접근할 때 로그인이 되어 있다면, 이 페이지로 이동하도록 함
    #    로그인이 되어있는지 확인:
    #       request.user.is_authenticated가 True인지 체크
    #
    # URL:      /posts/  (posts.urls를 사용, config.urls에서 include)
    #           app_name: 'posts'
    #           url name: 'post-list'
    #           -> posts:post-list
    # Template: templates/posts/post-list.html
    #           <h1>Post List</h1>

    # 'posts'라는 키로 모든 Post QuerySet을 전달
    #  (순서는 pk의 역순)
    # 그리고 전달받은 QuerySet을 순회하며 적절히 Post내용을 출력
    if tag is not None:
        posts = Post.objects.filter(tags__name__iexact=tag).order_by('-pk')
    else:
        posts = Post.objects.order_by('-pk')
    comment_form = CommentCreateForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/post-list.html', context)


#
# def post_list_by_tag(request, tag):
#     """
#     URL:        /explore/tags/<tag문자열>/
#     template:   /posts/post-list.html
#
#     <tag문자열>인 Tag를 자신(post).tags에 가지고 있는 경우의 Post 목록만 돌려줘야 함
#     이 내용 외에는 위의 post_list와 내용 동일
#
#     """
#     # URL: /explore/tags/<tag문자열>/
#     posts = Post.objects.filter(tags__name__iexact=tag).order_by('-pk')
#     comment_form = CommentCreateForm()
#     context = {
#         'posts': posts,
#         'comment_form': comment_form,
#     }
#     return render(request, 'posts/post-list.html', context)


def post_like(request, pk):
    """
    pk가 pk인 Post에 대한
    1. Postlike를 생성한다
    2. 만약 해당 객체가 이미 있다면, 삭제한다.
    3. posts:post_list로 redirect한다.
    :param request:
    :param pk:
    :return:
    """

    post = Post.objects.get(pk=pk)

    post_like_qs = PostLike.objects.filter(post=post, user=request.user)

    if post_like_qs.exists():
        post_like_qs.delete()

    else:
        PostLike.objects.create(post=post, user=request.user)

    return redirect('posts:post_list')

    # try:
    #     like1 = PostLike.objects.get(post=post, user=request.user)
    #     like1.delete()
    #
    #
    # except PostLike.DoesNotExist:
    #     like1 = PostLike.objects.create(post=post, user=request.user)
    #
    # return redirect('posts:post_list')


def post_create(request):
    """
    url:        /posts/create name='post-create'
    Template:   /posts/posts-create.html

    forms.PostCreateForm을 생성한다.

    :param request:
    :return:
    """

    if request.method == 'POST':
        images = request.FILES.getlist('image')
        content = request.POST['content']

        post = Post.objects.create(author=request.user, content=content)
        for image in images:
            print(image, type(image))
            post.postimage_set.create(image=image)

        return redirect('posts:post_list')
        pass
    else:
        form = PostCreateForm()
        context = {
            'form': form
        }
        return render(request, 'posts/post-create.html', context)


def comment_create(request, post_pk):
    # URL: /posts/<int:post_pk>/comments/create/
    # Template: 없음 (post-list.html내에 Form을 구현)
    #  post-list.html 내부에서, 각 Post마다 자신에게 연결된 PostComment목록을 보여주도록 함
    #   보여주는형식은
    #    <ul>
    #     <li><b>작성자명</b> <span>내용</span></li>
    #     <li><b>작성자명</b> <span>내용</span></li>
    #    </ul>
    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)
        # Form인스턴스를 만드는데, data에 request.POST로 전달된 dict를 입력
        form = CommentCreateForm(data=request.POST)
        # Form인스턴스 생성시, 주어진 데이터가
        # 해당 Form이 가진 Field들에 적절한 데이터인지 검증
        if form.is_valid():
            form.save(post=post, author=request.user)
        return redirect('posts:post_list')


def comment_list(request, post_pk):
    comments = PostComment.objects.filter(post=post_pk)
    return render(request, 'comment_list.html', context={'comments': comments})
