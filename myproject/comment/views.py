from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment
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


def news_cm_add(request, pk):

    if request.method == "POST":
        cm = request.POST.get("cm")

        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        today = str(year)+'/'+str(month)+'/'+str(day)
        time = str(hour)+':'+str(minute)

        if request.user.is_authenticated:
            manager = Manager.objects.get(utxt=request.user)
            b = Comment(name=manager.name, email=manager.email,
                        cm=cm, news_id=pk, date=today, time=time)
            b.save()
        else:
            name = request.POST.get("name")
            email = request.POST.get("email")
            cm = request.POST.get("cm")

            b = Comment(name=name, email=email, cm=cm,
                        news_id=pk, date=today, time=time)
            b.save()

    newsname = News.objects.get(pk=pk).name

    return redirect('home')


def comments_list(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":
            perm = 1

    if perm == 0:
        a = News.objects.get(pk=pk).writer
        if str(a) != str(request.user):
            error = "Access Denied.."
            return render(request, 'back/error.html', {'error': error})

    comments = Comment.objects.all()

    return render(request, 'back/comments_list.html', {'comments': comments})


def comments_del(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":
            perm = 1

    if perm == 0:
        a = News.objects.get(pk=pk).writer
        if str(a) != str(request.user):
            error = "Access Denied.."
            return render(request, 'back/error.html', {'error': error})

    comments = Comment.objects.get(pk=pk)
    comments.delete()

    return redirect('comments_list')


def comments_confirm(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":
            perm = 1

    if perm == 0:
        a = News.objects.get(pk=pk).writer
        if str(a) != str(request.user):
            error = "Access Denied.."
            return render(request, 'back/error.html', {'error': error})

    comments = Comment.objects.get(pk=pk)
    comments.status = 1
    comments.save()

    return redirect('comments_list')
