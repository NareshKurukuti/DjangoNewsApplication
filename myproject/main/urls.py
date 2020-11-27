from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^panel/$', views.panel, name='panel'),
    url(r'^login/$', views.mylogin, name='mylogin'),
    url(r'^logout/$', views.mylogout, name='mylogout'),
    url(r'^panel/settings/$', views.site_settings, name='site_settings'),
    url(r'^panel/about/settings/$', views.about_settings, name='about_settings'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^panel/change/pass/$', views.change_pass, name='change_pass'),
    url(r'^register/$', views.myregister, name='myregister'),
    url(r'^panel/answer/comments/(?P<pk>\d+)$', views.answer_cm, name='answer_cm'),
    url(r'^show/data/$', views.show_data, name='show_data'),
]
