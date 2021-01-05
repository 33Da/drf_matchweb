# Generated by Django 2.2 on 2020-02-07 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0010_auto_20200207_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='result',
        ),
        migrations.AddField(
            model_name='process',
            name='result',
            field=models.FileField(blank=True, help_text='比赛结果', null=True, upload_to='file/', verbose_name='比赛结果'),
        ),
    ]