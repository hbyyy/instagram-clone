from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    """

    :param request:
    :return:
    """
    return render(request, 'index.html')

