from django.shortcuts import render, get_object_or_404, redirect
from .models import BlackList
from main.models import Main
from django.core.files.storage import FileSystemStorage
import datetime
from subcat.models import SubCat
from cat.models import Cat
from news.models import News
from trending.models import Trending
from manager.models import Manager
import random

# Create your views here.


def black_list(request):

    ip = BlackList.objects.all()

    return render(request, 'back/blacklist.html', {'ip': ip})


def ip_add(request):

    if request.method == "POST":
        ip = request.POST.get('ip')

        if ip != "":

            b = BlackList(ip=ip)
            b.save()

    return redirect('black_list')


def ip_del(request, pk):

    b = BlackList.objects.filter(pk=pk)
    b.delete()

    return redirect('black_list')
