# Generated by Django 3.1.2 on 2020-11-02 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NBAstatsApp', '0005_auto_20201030_1059'),
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('action', models.CharField(max_length=200)),
                ('code', models.IntegerField()),
                ('clase', models.CharField(max_length=200)),
            ],
        ),
    ]
