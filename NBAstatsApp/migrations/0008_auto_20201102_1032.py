# Generated by Django 3.1.2 on 2020-11-02 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NBAstatsApp', '0007_auto_20201102_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assist',
            name='data',
            field=models.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='block',
            name='data',
            field=models.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='foul',
            name='data',
            field=models.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='point',
            name='data',
            field=models.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='rebound',
            name='data',
            field=models.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='steal',
            name='data',
            field=models.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='substitution',
            name='data',
            field=models.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='turnover',
            name='data',
            field=models.JSONField(default={}),
        ),
    ]