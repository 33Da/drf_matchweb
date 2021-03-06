# Generated by Django 2.2 on 2020-02-07 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0009_news_starttime'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='result',
            field=models.FileField(blank=True, help_text='比赛结果', null=True, upload_to='file/%Y%m%d', verbose_name='比赛结果'),
        ),
        migrations.AlterField(
            model_name='match',
            name='check',
            field=models.IntegerField(choices=[(0, '待审核'), (1, '审核通过'), (2, '审核不通过')], help_text='审核状态', verbose_name='审核状态'),
        ),
    ]
