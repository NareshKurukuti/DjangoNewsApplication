from django.shortcuts import render, get_object_or_404, redirect
from .models import Main
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
import random
import string
from ipware import get_client_ip
from ip2geotools.databases.noncommercial import DbIpCity
from blacklist.models import BlackList
from django.core.mail import send_mail
from django.conf import settings
from contactform.models import ContactForm
from zeep import Client
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
import urllib.request as urllib2
from rest_framework import viewsets
from .serializer import NewsSerializers
from django.http import JsonResponse
from newsletter.models import Newsletter



# Create your views here.

@csrf_exempt
def home(request):
    # sitename="My Site | Home"
    site = Main.objects.get(pk=4)
    sitename = site.name
    news = News.objects.filter(act=1).order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popnews = News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]

    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]

    # random_object = Trending.objects.all([randint(0, len(trending)-1)])

    #######################################################################
    
    # SOUP
    # client = Client('xxxxxx.wsdl')
    # result = client.service.funcname(1,2,3)
    # print(result)

    #######################################################################

    #Curl
    # url = 'xxxxxxxxxxxx'
    # payload = {'a' : "b", 'c' : "d"}
    # result = requests.post(url, params=payload)
    # print(result.url)
    # print(result)

    #######################################################################

    #Json
    # url = 'xxxxxxxxxxxxxxx'
    # data = {'a' : 'b', 'c' : 'd'}
    # headers = {'Content-Type':'application/json', 'API_KEY':'xxxxxxxxxx'}
    # result = request.post(url, data=json.dumps(data), 'headers'=headers)
    # print(result)

    #######################################################################

    # my_html = """
    #     <html>
    #     <head>
    #     <title> This is a Test </title>
    #         <mytag>My Tag</mytag>
    #     </head>
    #     <body>

    #     <h2>Submit Button</h2>

    #     <p class='test'>The <strong>input type="submit"</strong> defines a button for submitting form data to a form-handler:</p>

    #     <form action="/action_page.php">
    #     <label for="fname">First name:</label><br>
    #     <input type="text" id="fname" name="fname" value="John"><br>
    #     <label for="lname">Last name:</label><br>
    #     <input type="text" id="lname" name="lname" id="lname" value="Doe"><br><br>
    #     <input type="submit" value="Submit">
    #     </form> 

    #     <p>If you click "Submit", the form-data will be sent to a page called "/action_page.php".</p>

    #     </body>
    #     </html>
    # """

    # soup = BeautifulSoup(my_html, 'html.parser')
    # print(soup.title)
    # print(soup.title.string)
    # print(soup.mytag)
    # print(soup.mytag.string)

    # print(soup.p)
    # print(soup.p['class'])

    # print(soup.a)
    # print(soup.find_all('input'))
    # print(soup.find(id='lname'))

    # url = "https://www.w3schools.com/"
    # result = requests.post(url)
    # # print(result.content)
    # soup = BeautifulSoup(result.content, 'html.parser')
    # print(soup.title)


    #######################################################################
    # url = "https://www.w3schools.com/"
    # opener = urllib2.build_opener()
    # content = opener.open(url).read()
    # soup = BeautifulSoup(content, 'html.parser')
    # print(soup.title)

    #######################################################################
    # To Get the JSON Response
    # url = 'http://127.0.0.1:8000/show/data/'
    # opener = urllib2.build_opener()
    # content = opener.open(url).read()
    # print(content)

    return render(request, 'front/home.html', {'site': site, 'sitename': sitename, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews, 'popnews': popnews, 'popnews2': popnews2, 'trending': trending, 'lastnews2':lastnews2})


def about(request):
    # sitename = "My Site | About"
    site = Main.objects.get(pk=4)
    sitename = Main.objects.get(pk=4).name
    news = News.objects.filter(act=1).order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]

    return render(request, 'front/about.html', {'site': site, 'sitename': sitename, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews, 'popnews2': popnews2, 'trending': trending})


def panel(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    perm = 0
    perms = Permission.objects.filter(user=request.user)
    for i in perms:
        if i.codename == "master_user": perm = 1
    
    # if perm == 0 :
    #     error = "Access Denied.."
    #     return render(request, 'back/error.html', {'error': error})
    
    """
    # Generate 16 digit random string
    rand = ""
    for i in range(16):
        rand = rand + random.choice(string.ascii_letters)
    """

    """
    # Generate 12 Digit random string 
    test = ['!', '@', '#', '$', '%' ]
    rand = ""
    for i in range(4):
        rand = rand + random.choice(string.ascii_letters)
        rand += random.choice(test)
        rand += str(random.randinit(0,9))
    """
    """
    # Random Query
    count = News.objects.count()
    rand = News.objects.all()[random.randinit(0, count - 1)]
    """

    return render(request, 'back/home.html')


def mylogin(request):

    # if request.user.is_authenticated :
    #     return redirect('panel')

    if request.method == "POST":
        utxt = request.POST.get("username")
        ptxt = request.POST.get("password")

        if utxt != "" or ptxt != "":

            user = authenticate(username=utxt, password=ptxt)

            if user != None:

                login(request, user)
                return redirect('panel')

    return render(request, 'front/login.html')


def mylogout(request):
    logout(request)
    return redirect('mylogin')


def site_settings(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name =="masteruser" : perm = 1
    
    if perm == 0 :
        error = "Access Denied.."
        return render(request, 'back/error.html', {'error': error})

    if request.method == 'POST':
        name = request.POST.get('name')
        about = request.POST.get('about')
        fb = request.POST.get('fb')
        tw = request.POST.get('tw')
        yt = request.POST.get('yt')
        tell = request.POST.get('tell')
        link = request.POST.get('link')
        seo_txt = request.POST.get('seo_txt')
        seo_keywords = request.POST.get('seo_keywords')

        if fb == "":
            fb = "#"
        if tw == "":
            tw = "#"
        if yt == "":
            yt = "#"
        if link == "":
            link = "#"

        if name == "" or about == "" or tell == "":
            error = "Name, About and Tell are required"
            return render(request, 'back/error.html', {'error': error})

        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            picname = filename
            picurl = url
        except:
            picname = '-'
            picurl = '-'

        try:
            myfile2 = request.FILES['picnamefooter']
            fs2 = FileSystemStorage()
            filename2 = fs2.save(myfile2.name, myfile2)
            url2 = fs2.url(filename2)
            picname2 = filename2
            picurl2 = url2
        except:
            picname2 = '-'
            picurl2 = '-'

        b = Main.objects.get(pk=4)
        b.name = name
        b.about = about
        b.fb = fb
        b.tw = tw
        b.yt = yt
        b.link = link
        b.tell = tell
        b.seo_keywords=seo_keywords
        b.seo_txt=seo_txt
        if picname != "-":
            b.picname = picname
        if picurl != "-":
            b.picurl = picurl
        if picname != "-":
            b.picnamefooter = picname2
        if picurl2 != "-":
            b.picurlfooter = picurl2

        b.save()

    site = Main.objects.get(pk=4)

    return render(request, 'back/settings.html', {'site': site})


def about_settings(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name =="masteruser" : perm = 1
    
    if perm == 0 :
        error = "Access Denied.."
        return render(request, 'back/error.html', {'error': error})

    if request.method == 'POST':
        abouttxt = request.POST.get('abouttxt')

        if abouttxt == "":
            error = "About Text is required"
            return render(request, 'back/error.html', {'error': error})
        else:
            b = Main.objects.get(pk=4)
            b.abouttxt = abouttxt
            b.save()

    abouttxt = Main.objects.get(pk=4).abouttxt
    return render(request, 'back/about_settings.html', {'abouttxt': abouttxt})


def contact(request):
    # sitename = "My Site | About"
    site = Main.objects.get(pk=4)
    sitename = Main.objects.get(pk=4).name
    news = News.objects.filter(act=1).order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]

    return render(request, 'front/contact.html', {'site': site, 'sitename': sitename, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews, 'popnews2': popnews2, 'trending': trending})


def change_pass(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    if request.method == 'POST':

        oldpass = request.POST.get('oldpass')
        newpass = request.POST.get('newpass')

        if oldpass == "" or newpass == "":
            error = "All fields are required"
            return render(request, 'back/error.html', {'error': error})

        user = authenticate(username=request.user, password=oldpass)
        if user != None:
            # if len(newpass) < 8:
            #     error = "Your password must be at least 8 characters"
            #     return render(request, 'back/error.html', {'error': error})

            # count1 = 0
            # count2 = 0
            # count3 = 0
            # count4 = 0
            # for i in newpass:
            #     if i > "0" and i < "9":
            #         count1 = 1
            #     if i > "A" and i < "Z":
            #         count2 = 1
            #     if i > "a" and i < "z":
            #         count3 = 1
            #     if i > "!" and i < "(":
            #         count4 = 1
            # print(count1,count2,count3,count4)
            flag = 0
            while True:   
                if (len(newpass)<8): 
                    flag = -1
                    break
                elif not re.search("[a-z]", newpass): 
                    flag = -1
                    break
                elif not re.search("[A-Z]", newpass): 
                    flag = -1
                    break
                elif not re.search("[0-9]", newpass): 
                    flag = -1
                    break
                elif not re.search("[_@$]", newpass): 
                    flag = -1
                    break
                elif re.search("\s", newpass): 
                    flag = -1
                    break
                else: 
                    flag = 0 
                    break
            
            if flag ==-1: 
                error = "Your password must be at least one Special Character, one Capital Letter, one Small Letter, one Digit and must be minimum 8 characters"
                return render(request, 'back/error.html', {'error': error})
            else :
                user = User.objects.get(username=request.user)
                user.set_password(newpass)
                user.save()
                return redirect("mylogout")                
        else:
            error = "Your password is not Correct"
            return render(request, 'back/error.html', {'error': error})

    return render(request, 'back/changepass.html')


def myregister(request):

    if request.method == "POST":
        name = request.POST.get("name")
        uname = request.POST.get("uname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if name == "":
            msg = "Enter Your Name"
            return render(request, "front/msgbox.html", {'msg':msg})

        if password != password2:
            msg = "Your password didn't match"
            return render(request, "front/msgbox.html", {'msg':msg})
        flag = 0
        while True:   
            if (len(password)<8): 
                flag = -1
                break
            elif not re.search("[a-z]", password): 
                flag = -1
                break
            elif not re.search("[A-Z]", password): 
                flag = -1
                break
            elif not re.search("[0-9]", password): 
                flag = -1
                break
            elif not re.search("[_@$]", password): 
                flag = -1
                break
            elif re.search("\s", password): 
                flag = -1
                break
            else: 
                flag = 0 
                break
        
        if flag ==-1: 
            msg = "Your password must be at least one Special Character, one Capital Letter, one Small Letter, one Digit and must be minimum 8 characters"
            return render(request, "front/msgbox.html", {'msg':msg})
        
        if len(User.objects.filter(username=uname)) == 0 and len(User.objects.filter(email=email)) == 0:
            ip, is_routable = get_client_ip(request)
            if ip is None :
                ip = "0.0.0.0"
            
            try :
                response = DbIpCity.get(ip, api_key="free")
                country = response.country + " | "+ response.city
            except:
                country = "Unknown"
            
            user = User.objects.create_user(username=uname, email=email, password=password)
            b = Manager(name=name,utxt=uname, email=email,ip=ip,country=country)
            b.save()
        else:
            msg = "Username and Email Already Exist.."
            return render(request, "front/msgbox.html", {'msg':msg})
    return render(request, 'front/login.html')

def answer_cm(request, pk):

    if request.method == "POST":
        txt = request.POST.get("txt")

        if txt == "":
            error = "Type Your Answer"
            return render(request, "back/error.html", {'error':error})

        to_email = ContactForm.objects.get(pk=pk).email
        
        # To Send Emails With Configured Settings
        """
        subject = 'answer form'
        message = txt
        email_from = settings.EMAIL_HOST_USER
        emails = [to_email]
        send_mail(subject,message,email_form,emails)
        """
        send_mail(
            'sender number',
            txt,
            'reply@k.com',
            ['kurukuti.naresh@7edge.com'],
            fail_silently=False,
        )

    return render(request, 'back/answer_cm.html', {'pk' : pk})



class NewsViewSet(viewsets.ModelViewSet):

    queryset = News.objects.all()
    serializer_class = NewsSerializers






def show_data(request):
    count = Newsletter.objects.filter(status=1).count()
    data = {'count' :count}
    return JsonResponse(data)