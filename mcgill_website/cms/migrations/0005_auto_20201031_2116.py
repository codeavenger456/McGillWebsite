# Generated by Django 2.2.12 on 2020-10-31 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0004_auto_20201031_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='paage_title_en',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='page',
            name='page_title_fr',
            field=models.TextField(blank=True, default=''),
        ),
    ]
