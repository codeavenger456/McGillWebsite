# Generated by Django 3.1.3 on 2020-12-08 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0015_auto_20201208_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='english_title',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='news',
            name='french_title',
            field=models.TextField(blank=True, default=''),
        ),
    ]
