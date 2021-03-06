# Generated by Django 3.1.3 on 2020-11-26 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0008_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=200)),
                ('job_id', models.IntegerField()),
                ('short_description', models.TextField(blank=True, default='')),
                ('long_description', models.TextField(blank=True, default='')),
            ],
        ),
    ]
