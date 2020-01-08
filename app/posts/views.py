from django.shortcuts import render, redirect

# Create your views here.
from posts.forms import PostCreateForm, CommentCreateForm
from posts.models import Post, PostLike, PostImage


def post_list(request):
    # URL = /posts/
    # template: templates/posts/post-list.html
    posts = Post.objects.order_by('-pk')
    form = CommentCreateForm()
    context = dict(posts=posts, form=form)

    return render(request, 'posts/post-list.html', context)


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
            PostImage.objects.create(post=post, image=image)

        return redirect('posts:post_list')

    else:
        form = PostCreateForm()
        context = {
            'form': form
        }
        return render(request, 'posts/post-create.html', context)


def comment_create(request, post_pk):
    """
    url : /posts/<int:post_pk>/comments/create/
    Template: dqjtdma(post-list.html에 Form을 구현)
    post-list.html 내부에서, 각 Post마다 자신에게 연결된 PostComment목록을 보여주도록 한다
        <ul>
            <li><b>작성자명</b><span>내용</span></li>
            <li><b>작성자명</b><span>내용</span></li>
        </ul>
    Form: post.forms.CommentCreateForm
    :param request:
    :param post_pk:
    :return:
    """
    if request.method == 'POST':
        user = request.user
        post = Post.objects.get(pk=post_pk)
        # content = request.POST['content']
        # Form instance를 만드는데, data에 request.POST로 전달된 dict를 입력
        form = CommentCreateForm(data=request.POST)
        # Form 인스턴스 생성시, 주어진 데이터가 해당 Form이 가진 Field들에 적절한 데이터인지 검증
        if form.is_valid():
            # 검증에 통과한 경우, 통과한 데이터들은 Form 인스턴스의 'cleaned_date속성에 포함됨
            # content = form.cleaned_data['content']
            # PostComment.objects.create(
            #     author=user,
            #     post=post,
            #     content=content

            form.save(post=post, author=request.user)

        return redirect('posts:post_list')
