# Generated by Django 3.2.12 on 2022-05-26 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0004_advertisement_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='website',
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
    ]
