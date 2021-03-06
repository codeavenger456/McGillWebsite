# Generated by Django 3.1.3 on 2020-12-08 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0014_news'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='eventDay',
        ),
        migrations.RemoveField(
            model_name='event',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='event',
            name='title',
        ),
        migrations.AddField(
            model_name='event',
            name='end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='english_description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='event',
            name='english_section',
            field=models.CharField(default='section', max_length=50),
        ),
        migrations.AddField(
            model_name='event',
            name='english_title',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='event',
            name='french_description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='event',
            name='french_section',
            field=models.CharField(default='section', max_length=50),
        ),
        migrations.AddField(
            model_name='event',
            name='french_title',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='event',
            name='start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
