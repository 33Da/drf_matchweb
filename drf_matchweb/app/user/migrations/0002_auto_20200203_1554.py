# Generated by Django 2.2 on 2020-02-03 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='major',
            name='name',
            field=models.CharField(default='', help_text='专业名', max_length=30, verbose_name='专业名'),
        ),
    ]