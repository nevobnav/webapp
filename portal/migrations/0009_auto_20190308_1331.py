# Generated by Django 2.1.7 on 2019-03-08 13:31

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0008_auto_20190306_0727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plot',
            name='customer',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='portal.Customer'),
        ),
        migrations.AlterField(
            model_name='plot',
            name='startdate',
            field=models.DateField(default=datetime.date(2019, 3, 8)),
        ),
        migrations.AlterField(
            model_name='scan',
            name='date',
            field=models.DateField(default=datetime.date(2019, 3, 8)),
        ),
    ]
