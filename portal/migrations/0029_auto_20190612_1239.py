# Generated by Django 2.1.7 on 2019-06-12 12:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0028_auto_20190610_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plot',
            name='crop',
            field=models.CharField(choices=[('BROCCOLI', 'Broccoli'), ('BLOEMKOOL', 'Bloemkool'), ('TULP', 'Tulpen'), ('LELY', 'Lelies'), ('HYACINTH', 'Hyacinth'), ('CICHOREI', 'Cichorei'), ('AARDAPPEL', 'Aardappelen'), ('SPRUIT', 'Spruiten'), ('SLA', 'Sla'), ('PEEN', 'Peen'), ('UI', 'Ui')], default='None', max_length=100),
        ),
        migrations.AlterField(
            model_name='plot',
            name='startdate',
            field=models.DateField(default=datetime.date(2019, 6, 12)),
        ),
        migrations.AlterField(
            model_name='scan',
            name='date',
            field=models.DateField(default=datetime.date(2019, 6, 12)),
        ),
        migrations.AlterField(
            model_name='scan',
            name='sensor',
            field=models.CharField(default='unknown', max_length=100),
        ),
    ]
