from django.shortcuts import render, redirect

# Create your views here.
from posts.forms import PostCreateForm
from posts.models import Post, PostLike, PostImage


def post_list(request):
    # URL = /posts/
    # template: templates/posts/post-list.html
    posts = Post.objects.order_by('-pk')
    context = dict(posts=posts)

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
        image = request.FILES['image']
        content = request.POST['content']

        post = Post.objects.create(author=request.user, content=content)
        postimage = PostImage.objects.create(post=post, image=image)

        return redirect('posts:post_list')
        pass
    else:
        form = PostCreateForm()
        context = {
            'form': form
        }
        return render(request, 'posts/post-create.html', context)
