# Generated by Django 3.2.12 on 2022-05-26 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_user_isgeneral'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='blog_url',
            field=models.URLField(blank=True, max_length=300, null=True),
        ),
    ]