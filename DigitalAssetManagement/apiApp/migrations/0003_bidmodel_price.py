# Generated by Django 4.1.7 on 2023-04-01 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apiApp", "0002_bidmodel"),
    ]

    operations = [
        migrations.AddField(
            model_name="bidmodel",
            name="price",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
