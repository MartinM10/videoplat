# Generated by Django 2.2 on 2019-05-07 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_auto_20190506_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='views',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
