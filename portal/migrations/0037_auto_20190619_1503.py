# Generated by Django 2.1.7 on 2019-06-19 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0036_mapnote_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapnote',
            name='note',
            field=models.TextField(null=True),
        ),
    ]
