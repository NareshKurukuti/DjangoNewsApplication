# Generated by Django 3.1.3 on 2020-11-12 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20201112_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='main',
            name='fb',
            field=models.TextField(default='-'),
        ),
        migrations.AddField(
            model_name='main',
            name='tw',
            field=models.TextField(default='-'),
        ),
        migrations.AddField(
            model_name='main',
            name='yt',
            field=models.TextField(default='-'),
        ),
    ]
