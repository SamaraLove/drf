# Generated by Django 3.0.8 on 2020-10-06 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20200904_2004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='rating',
        ),
    ]
