# Generated by Django 3.0.8 on 2020-08-28 09:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20200828_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
    ]
