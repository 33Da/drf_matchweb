# Generated by Django 2.2 on 2020-02-04 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0004_auto_20200204_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='endtime',
            field=models.DateField(help_text='流程结束时间', verbose_name='流程结束时间'),
        ),
        migrations.AlterField(
            model_name='process',
            name='starttime',
            field=models.DateField(help_text='流程开始时间', verbose_name='流程开始时间'),
        ),
    ]