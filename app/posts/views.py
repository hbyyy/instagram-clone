from django.shortcuts import render


# Create your views here.
from posts.models import Post


def post_list(request):
    # URL = /posts/
    # template: templates/posts/post-list.html
    posts = Post.objects.order_by('-pk')
    context = dict(posts=posts)

    return render(request, 'posts/post-list.html', context)
