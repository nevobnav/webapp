# Generated by Django 2.1.7 on 2019-06-19 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0034_auto_20190619_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapnote',
            name='lat',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='mapnote',
            name='lon',
            field=models.FloatField(null=True),
        ),
    ]
