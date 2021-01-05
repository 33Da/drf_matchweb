# Generated by Django 2.2 on 2020-02-01 21:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('match', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useandmatch',
            name='user',
            field=models.ForeignKey(help_text='用户', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='process',
            name='match',
            field=models.ForeignKey(help_text='比赛', on_delete=django.db.models.deletion.CASCADE, related_name='process', to='match.Match', verbose_name='比赛'),
        ),
        migrations.AddField(
            model_name='match',
            name='type',
            field=models.ForeignKey(help_text='比赛类型', on_delete=django.db.models.deletion.CASCADE, to='match.Type', verbose_name='比赛类型'),
        ),
        migrations.AddField(
            model_name='match',
            name='user',
            field=models.ManyToManyField(blank=True, help_text='报名人', null=True, related_name='my_match', through='match.UseAndMatch', to=settings.AUTH_USER_MODEL, verbose_name='报名人'),
        ),
    ]