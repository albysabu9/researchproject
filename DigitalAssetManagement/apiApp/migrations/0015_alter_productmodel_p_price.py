# Generated by Django 4.1.7 on 2023-11-25 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apiApp", "0014_alter_blockchainmodel_block"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productmodel",
            name="p_price",
            field=models.FloatField(default=None, null=True),
        ),
    ]