# Generated by Django 2.2.3 on 2019-10-10 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20191011_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='num_followers',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
