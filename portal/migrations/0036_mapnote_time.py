# Generated by Django 2.1.7 on 2019-06-19 14:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0035_auto_20190619_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapnote',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]