# Generated by Django 2.2.12 on 2020-10-31 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20201031_2108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='unique_id',
        ),
        migrations.AddField(
            model_name='page',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='page',
            name='page_name_en',
            field=models.CharField(default='', max_length=200),
        ),
    ]