# Generated by Django 2.1.7 on 2019-07-08 13:34

import datetime
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0046_auto_20190621_0909'),
    ]

    operations = [
        migrations.CreateModel(
            name='Datalayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(null=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('property_name', models.CharField(max_length=256, null=True)),
                ('layer_name', models.CharField(max_length=256, null=True)),
                ('legend_title', models.CharField(max_length=256, null=True)),
                ('legend_unit', models.CharField(max_length=256, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='plot',
            name='startdate',
            field=models.DateField(default=datetime.date(2019, 7, 8)),
        ),
        migrations.AlterField(
            model_name='scan',
            name='date',
            field=models.DateField(default=datetime.date(2019, 7, 8)),
        ),
        migrations.AddField(
            model_name='datalayer',
            name='scan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='portal.Scan'),
        ),
    ]