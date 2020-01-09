from django.http import HttpResponse
from django.shortcuts import render, redirect

from members.models import User


# def index(request):
#     """
#
#     :param request:
#     :return:
#     """
#
#     if request.user.is_authenticated is True:
#         return redirect('posts:post_list')
#         # return render(request, 'posts/post-list.html')
#
#     else:
#         return render(request, 'index.html')
#
