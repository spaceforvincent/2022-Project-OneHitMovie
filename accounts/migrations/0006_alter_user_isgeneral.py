# Generated by Django 3.2.12 on 2022-05-21 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_isgeneral'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='isgeneral',
            field=models.CharField(choices=[('1', '일반 회원'), ('0', '판매 회원')], max_length=10),
        ),
    ]