# Generated by Django 2.2 on 2020-02-05 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0005_auto_20200204_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='useandmatch',
            name='group',
            field=models.CharField(blank=True, help_text='小组', max_length=300, null=True, verbose_name='小组'),
        ),
    ]
