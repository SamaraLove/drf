# Generated by Django 3.0.8 on 2020-09-03 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20200902_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=models.URLField(default='', max_length=400),
        ),
    ]
