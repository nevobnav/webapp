# Generated by Django 2.1.7 on 2019-05-31 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0019_auto_20190531_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plot',
            name='startdate',
            field=models.DateField(default='2019-05-01'),
        ),
    ]
