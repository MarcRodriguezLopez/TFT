# Generated by Django 3.1.2 on 2021-01-19 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NBAstatsApp', '0011_auto_20210119_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='standing',
            name='part',
            field=models.CharField(max_length=200),
        ),
    ]
