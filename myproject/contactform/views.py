from django.shortcuts import render, get_object_or_404, redirect
from .models import ContactForm
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
import datetime


# Create your views here.

def contact_add(request):

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

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        website = request.POST.get("website")
        message = request.POST.get("message")

        if name == "" or email == "" or website == "" or message == "":
            msg = "All fields are required"
            return render(request, 'front/msgbox.html', {'msg': msg})

        b = ContactForm(name=name, email=email,website=website, message=message, date=today, time=time)
        b.save()
        msg = 'Your Message Received..'

        return render(request, 'front/msgbox.html', {'msg': msg})

    return render(request, 'front/msgbox.html')


def contact_show(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    contacts = ContactForm.objects.all()

    return render(request, 'back/contactform.html', {'contacts': contacts})


def contact_delete(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end

    try:
        b = ContactForm.objects.get(pk=pk)
        b.delete()
    except:
        error = "Something Went Wrong.."
        return render(request, 'back/error.html', {'error': error})
    return redirect('contact_show')
