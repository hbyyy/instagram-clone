from django.shortcuts import render


# Create your views here.


def post_list(request):
    # URL = /posts/
    # template: templates/posts/post-list.html
    return render(request, 'posts/post-list.html')
