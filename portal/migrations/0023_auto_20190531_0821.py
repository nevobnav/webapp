# Generated by Django 2.1.7 on 2019-05-31 08:21

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0022_auto_20190531_0810'),
    ]

    operations = [
        migrations.AddField(
            model_name='plot',
            name='starting_point',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name='plot',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]