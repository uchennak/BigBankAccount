# Generated by Django 2.2 on 2020-12-09 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_auto_20201208_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account_balance',
            field=models.IntegerField(),
        ),
    ]
