from django.conf.urls import url
from . import views

urlpatterns =[
    url(r'^news/(?P<word>.*)/$', views.news_detail, name='news_detail'),
    url(r'^panel/news/list/$', views.news_list, name='news_list'),
    url(r'^panel/news/add/$', views.news_add, name='news_add'),
    url(r'^panel/news/delete/(?P<pk>\d+)/$', views.news_delete, name='news_delete'),
    url(r'^panel/news/edit/(?P<pk>\d+)/$', views.news_edit, name='news_edit'),
    url(r'^panel/news/publish/(?P<pk>\d+)/$', views.news_publish, name='news_publish'),
    url(r'^all/news/(?P<word>.*)/$', views.news_all_show, name='news_all_show'),
    url(r'^allcategroies/news/$', views.news_all_categories, name='news_all_categories'),
    url(r'^search/news/$', views.news_all_search, name='news_all_search'),
]