# Generated by Django 2.1.7 on 2019-05-20 13:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0015_auto_20190513_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='scan',
            name='zoomlevel',
            field=models.PositiveSmallIntegerField(default=23),
        ),
        migrations.AlterField(
            model_name='plot',
            name='startdate',
            field=models.DateField(default=datetime.date(2019, 5, 20)),
        ),
        migrations.AlterField(
            model_name='scan',
            name='date',
            field=models.DateField(default=datetime.date(2019, 5, 20)),
        ),
    ]
