# Generated by Django 3.2.23 on 2024-01-05 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_auto_20240105_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='num_of_containers',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
