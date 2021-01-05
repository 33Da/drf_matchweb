# Generated by Django 2.2 on 2020-02-06 21:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0007_useandmatch_check'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='match',
            field=models.ForeignKey(default=1, help_text='评论竞赛', on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='match.Match', verbose_name='评论竞赛'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(help_text='评论用户', on_delete=django.db.models.deletion.CASCADE, related_name='comment', to=settings.AUTH_USER_MODEL, verbose_name='评论用户'),
        ),
    ]
