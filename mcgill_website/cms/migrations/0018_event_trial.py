# Generated by Django 3.1.3 on 2020-12-08 13:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0017_auto_20201208_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='trial',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
