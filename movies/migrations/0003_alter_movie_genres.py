# Generated by Django 3.2.12 on 2022-05-21 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_moviecomment_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(related_name='genres', to='movies.Genre'),
        ),
    ]
