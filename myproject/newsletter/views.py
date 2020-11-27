from django.shortcuts import render, get_object_or_404, redirect
from .models import Newsletter
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from trending.models import Trending
import random
from random import randint
from django.contrib.auth.models import User, Group, Permission
import re
from manager.models import Manager
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.


def news_letter(request):

    if request.method == "POST":

        txt = request.POST.get("txt")
        res = txt.find('@')

        if int(res) != -1:
            b = Newsletter(txt=txt, status=1)
            b.save()
        else:
            try:
                int(txt)
                b = Newsletter(txt=txt, status=2)
                b.save()
            except:
                return redirect('home')
    return redirect('home')


def news_emails(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    emails = Newsletter.objects.filter(status=1)
    return render(request, 'back/emails.html', {'emails': emails})


def news_phones(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    phones = Newsletter.objects.filter(status=2)
    return render(request, 'back/phones.html', {'phones': phones})


def newsletter_del(request, pk, status):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    newsletter = Newsletter.objects.get(pk=pk)
    newsletter.delete()

    if int(status) == 1:
        return redirect('news_emails')
    elif int(status) == 2:
        return redirect('news_phones')

def send_email(request):

    if request.method == "POST":
        txt = request.POST.get("txt")

        to_email = []
        for i in Newsletter.objects.all():
            to_email.append(Newsletter.objects.get(pk=i.pk).txt)
        
        """
        subject = 'Message'
        message = txt
        email_from = settings.EMAIL_HOST_USER
        emails = [to_email]
        send_mail(subject,message,email_form,emails)
        """
    return redirect('news_emails')

def check_mychecklist(request):

    if request.method == "POST":

        # for i in Newsletter.objects.filter(status=1):
        #     x = request.POST.get(str(i.pk))
        #     if str(x) == "on":
        #         b = Newsletter.objects.get(pk=i.pk)
        #         b.delete()

        selectedRecords = request.POST.getlist('checks[]')
        for i in selectedRecords:
            b = Newsletter.objects.get(pk=i)
            b.delete()

    return redirect('news_emails')