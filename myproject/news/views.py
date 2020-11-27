from django.shortcuts import render, get_object_or_404, redirect
from .models import News
from main.models import Main
from django.core.files.storage import FileSystemStorage
import datetime
from subcat.models import SubCat
from cat.models import Cat
from trending.models import Trending
import random
from comment.models import Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain



# Create your views here.


def news_detail(request, word):
    # # login check start
    # if not request.user.is_authenticated:
    #     return redirect('mylogin')
    # # login check end

    site = Main.objects.get(pk=4)
    sitename = site.name
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    popnews = News.objects.all().order_by('-show')
    popnews2 = News.objects.all().order_by('-show')[:3]

    shownews = News.objects.filter(name=word)
    tagnames = News.objects.get(name=word).tag
    tag = tagnames.split(',')
    trending = Trending.objects.all().order_by('-pk')

    try :
        mynews = News.objects.get(name=word)
        mynews.show = mynews.show + 1
        mynews.save()
    except:
        print("Can't add show")

    code = News.objects.get(name=word).pk
    comments = Comment.objects.filter(news_id=code, status=1).order_by('-pk')[:3]
    comments_count = len(comments)

    return render(request, 'front/news_detail.html', {'site': site, 'sitename': sitename, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews, 'shownews': shownews, 'popnews':popnews, 'popnews2':popnews2, 'tag':tag, 'trending':trending, 'code':code, 'comments' :comments, 'comments_count':comments_count, 'tagnames': tagnames})


def news_list(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1
    
    if perm == 0:
        news = News.objects.filter(writer=request.user).order_by("pk")
    elif perm == 1:
        # news = News.objects.all().order_by("pk")
        newss = News.objects.all()
        paginator = Paginator(newss, 2)
        page = request.GET.get('page')

        try:
            news = paginator.page(page)

        except EmptyPage:
            news = paginator.page(paginator.num_page)
        
        except PageNotAnInteger:
            news = paginator.page(1)

    return render(request, 'back/news_list.html', {'news': news})


def news_add(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute

    if len(str(month)) == 1:
        month = "0"+month
    if len(str(day)) == 1:
        day = "0"+day

    today = str(year)+'/'+str(month)+'/'+str(day)
    time = str(hour)+':'+str(minute)

    date = str(year) + str(month) + str(day)
    randint = str(random.randint(1000, 9999))
    rand = date+randint
    rand = int(rand)

    while len(News.objects.filter(rand=rand)) != 0:
        randint = str(random.randint(1000, 9999))
        rand = date+randint
        rand = int(rand)



    cat = SubCat.objects.all()

    if request.method == 'POST':
        newstitle = request.POST.get('newstitle')
        newscat = request.POST.get('newscat')
        newstxtshort = request.POST.get('newstxtshort')
        newstxt = request.POST.get('newstxt')
        newsid = request.POST.get('newscat')
        tag = request.POST.get('tag')

        if newstitle == "" or newstxtshort == "" or newstxt == "" or newscat == "":
            error = "All fields are required"
            return render(request, 'back/error.html', {'error': error})

        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith("image"):
                if myfile.size < 2000000:
                    newsname = SubCat.objects.get(pk=newsid).name
                    ocatid = SubCat.objects.get(pk=newsid).category_id
                    b = News(name=newstitle, short_text=newstxtshort, body_text=newstxt, date=today, picname=filename,picurl=url, writer=request.user, catname=newsname, catid=newsid, show=0, time=time, ocatid=ocatid, tag=tag,rand=rand)
                    b.save()

                    count = len(News.objects.filter(ocatid=ocatid))

                    b = Cat.objects.get(pk=ocatid)
                    b.count = count
                    b.save()
                else:
                    fs.delete(filename)
                    error = "File size must be lessthan 2MB"
                    return render(request, 'back/error.html', {'error': error})
            else:
                fs.delete(filename)
                error = "Your File not supported,  Please select Image only.."
                return render(request, 'back/error.html', {'error': error})
        except:
            error = "Please select Your File"
            return render(request, 'back/error.html', {'error': error})

        return redirect(news_list)

    return render(request, 'back/news_add.html', {'cat': cat})


def news_delete(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1
    
    if perm == 0:
        a = News.objects.get(pk=pk).writer
        if str(a) !=  str(request.user) :
            error = "Access Denied.."
            return render(request, 'back/error.html', {'error': error})

    try:
        b = News.objects.get(pk=pk)

        fs = FileSystemStorage()
        fs.delete(b.picname)

        ocatid = News.objects.get(pk=pk).ocatid

        b.delete()

        count = len(News.objects.filter(ocatid=ocatid))

        m = Cat.objects.get(pk=ocatid)
        m.count = count
        m.save()
    except:
        error = "Something Went Wrong.."
        return render(request, 'back/error.html', {'error': error})

    return redirect('news_list')


def news_edit(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    if len(News.objects.filter(pk=pk)) == 0:
        error = "News Not Found.."
        return render(request, 'back/error.html', {'error': error})

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1
    
    if perm == 0:
        a = News.objects.get(pk=pk).writer
        if str(a) !=  str(request.user) :
            error = "Access Denied.."
            return render(request, 'back/error.html', {'error': error})

    news = News.objects.get(pk=pk)
    cat = SubCat.objects.all()

    if request.method == 'POST':
        newstitle = request.POST.get('newstitle')
        newscat = request.POST.get('newscat')
        newstxtshort = request.POST.get('newstxtshort')
        newstxt = request.POST.get('newstxt')
        newsid = request.POST.get('newscat')
        tag = request.POST.get('tag')

        if newstitle == "" or newstxtshort == "" or newstxt == "" or newscat == "":
            error = "All fields are required"
            return render(request, 'back/error.html', {'error': error})

        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith("image"):
                if myfile.size < 2000000:
                    newsname = SubCat.objects.get(pk=newsid).name

                    b = News.objects.get(pk=pk)

                    fss = FileSystemStorage()
                    fss.delete(b.picname)

                    b.name = newstitle
                    b.short_text = newstxtshort
                    b.body_text = newstxt
                    b.picname = filename
                    b.picurl = url
                    b.catname = newsname
                    b.catid = newsid
                    b.tag = tag
                    b.act = 0

                    b.save()
                else:
                    fs.delete(filename)
                    error = "File size must be lessthan 2MB"
                    return render(request, 'back/error.html', {'error': error})
            else:
                fs.delete(filename)
                error = "Your File not supported,  Please select Image only.."
                return render(request, 'back/error.html', {'error': error})
        except:
            newstitle = request.POST.get('newstitle')
            newscat = request.POST.get('newscat')
            newstxtshort = request.POST.get('newstxtshort')
            newstxt = request.POST.get('newstxt')
            newsid = request.POST.get('newscat')
            newsname = SubCat.objects.get(pk=newsid).name
            tag = request.POST.get('tag')

            b = News.objects.get(pk=pk)
            b.name = newstitle
            b.short_text = newstxtshort
            b.body_text = newstxt
            b.catname = newsname
            b.catid = newsid
            b.tag = tag
            b.act = 0

            b.save()

        return redirect(news_list)

    return render(request, 'back/news_edit.html', {'pk': pk, 'cat': cat, 'news': news})


def news_publish(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    try:
        b = News.objects.get(pk=pk)
        b.act = 1
        b.save()

        # fs = FileSystemStorage()
        # fs.delete(b.picname)

        # ocatid = News.objects.get(pk=pk).ocatid

        # b.delete()

        # count = len(News.objects.filter(ocatid=ocatid))

        # m = Cat.objects.get(pk=ocatid)
        # m.count = count
        # m.save()
    except:
        error = "Something Went Wrong.."
        return render(request, 'back/error.html', {'error': error})

    return redirect('news_list')


def news_all_show(request, word):

    catid = Cat.objects.get(name=word).pk
    catname = Cat.objects.get(name=word).name
    allnews = News.objects.filter(ocatid=catid)

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

    return render(request, 'front/all_news.html', {'site': site, 'sitename': sitename, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews, 'popnews': popnews, 'popnews2': popnews2, 'trending': trending, 'lastnews2':lastnews2, 'allnews' : allnews, 'catname':catname})

def news_all_categories(request):
    
    allnews = News.objects.all()

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


    paginator = Paginator(allnews, 6)
    page = request.GET.get('page')

    try:
        allnews = paginator.page(page)

    except EmptyPage:
        allnews = paginator.page(paginator.num_page)
    
    except PageNotAnInteger:
        allnews = paginator.page(1)

    return render(request, 'front/news_all_categories.html', {'site': site, 'sitename': sitename, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews, 'popnews': popnews, 'popnews2': popnews2, 'trending': trending, 'lastnews2':lastnews2, 'allnews' : allnews})


# Global Variables
searchData = ''

def news_all_search(request):
    
    if request.method == "POST" :
        txt = request.POST.get('txt')
        catid = request.POST.get('cat')
        date = str(request.POST.get('date'))
        year, month, day = date.split('-')
        selectedDate = str(year)+'/'+str(month)+'/'+str(day)

        if txt != "" and catid != "" and date != "" :
            a = News.objects.filter(name__contains=txt,ocatid=catid,date__gte=selectedDate)
            b = News.objects.filter(short_text__contains=txt,ocatid=catid,date__gte=selectedDate)
            c = News.objects.filter(body_text__contains=txt,ocatid=catid,date__gte=selectedDate)
        elif txt !="" and catid != "" and date == "" :
            a = News.objects.filter(name__contains=txt,ocatid=catid)
            b = News.objects.filter(short_text__contains=txt,ocatid=catid)
            c = News.objects.filter(body_text__contains=txt,ocatid=catid)
        elif txt !="" and catid == "" and date != "" :
            a = News.objects.filter(name__contains=txt,date__gte=selectedDate)
            b = News.objects.filter(short_text__contains=txt,date__gte=selectedDate)
            c = News.objects.filter(body_text__contains=txt,date__gte=selectedDate)
        elif txt =="" and catid != "" and date != "" :
            a = News.objects.filter(ocatid=catid,date__gte=selectedDate)
            b = News.objects.filter(ocatid=catid,date__gte=selectedDate)
            c = News.objects.filter(ocatid=catid,date__gte=selectedDate)
        else:
            a = News.objects.filter(name__contains=txt)
            b = News.objects.filter(short_text__contains=txt)
            c = News.objects.filter(body_text__contains=txt)
    else:
        a = News.objects.filter(name__contains=txt)
        b = News.objects.filter(short_text__contains=txt)
        c = News.objects.filter(body_text__contains=txt)

    allnews = list(chain(a, b, c))
    allnews = list(dict.fromkeys(allnews)) #for getting unique records

    site = Main.objects.get(pk=4)
    sitename = site.name
    news = News.objects.filter(act=1).order_by('-pk')
    cat = Cat.objects.all()
    if catid != "0":
        selectedCategoryName = Cat.objects.get(pk=catid).name
    else:
        selectedCategoryName = "0"
    subcat = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popnews = News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]
    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]


    # paginator = Paginator(allnews, 3)
    # page = request.GET.get('page')

    # try:
    #     allnews = paginator.page(page)

    # except EmptyPage:
    #     allnews = paginator.page(paginator.num_page)
    
    # except PageNotAnInteger:
    #     allnews = paginator.page(1)

    return render(request, 'front/news_all_categories.html', {'site': site, 'sitename': sitename, 'news': news, 'cat': cat, 'subcat': subcat, 'lastnews': lastnews, 'popnews': popnews, 'popnews2': popnews2, 'trending': trending, 'lastnews2':lastnews2, 'allnews' : allnews, 'txt' : txt, 'catid':catid, 'selectedCategoryName': selectedCategoryName, 'date':date})


# News.objects.filter(pk=pk).exclude(date__gte="2019/01/01")