# Generated by Django 2.1.7 on 2019-04-09 13:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0013_auto_20190408_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plot',
            name='startdate',
            field=models.DateField(default=datetime.date(2019, 4, 9)),
        ),
        migrations.AlterField(
            model_name='scan',
            name='date',
            field=models.DateField(default=datetime.date(2019, 4, 9)),
        ),
    ]