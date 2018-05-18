# Generated by Django 2.0.2 on 2018-05-18 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offline_calculator', '0011_auto_20180518_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrepositories',
            name='contributions',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterModelTable(
            name='user',
            table='users',
        ),
        migrations.AlterModelTable(
            name='userrepositories',
            table='user_repositories',
        ),
    ]
