from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^newsletter/add/$', views.news_letter, name='news_letter'),
    url(r'^panel/newsletter/emails/$', views.news_emails, name='news_emails'),
    url(r'^panel/newsletter/phones/$', views.news_phones, name='news_phones'),
    url(r'^panel/newsletter/del/(?P<pk>\d+)/(?P<status>\d+)/$', views.newsletter_del, name='newsletter_del'),
    url(r'^panel/newsletter/sendemail/$', views.send_email, name='send_email'),
    url(r'^newsletter/check/checklist/$', views.check_mychecklist, name='check_mychecklist'),
]
