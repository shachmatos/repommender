# Generated by Django 2.0.2 on 2018-04-28 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offline_calculator', '0002_auto_20180428_1230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='id',
        ),
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
