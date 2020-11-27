from rest_framework import serializers
from news.models import News



class NewsSerializers(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = News
        fields = ['name', 'date', 'picurl', 'writer']

