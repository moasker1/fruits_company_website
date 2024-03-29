# Generated by Django 3.2.23 on 2024-01-06 13:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0022_remove_container_num_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='date',
            field=models.DateField(default=datetime.date(2024, 1, 6)),
        ),
        migrations.AlterField(
            model_name='seller',
            name='date',
            field=models.DateField(default=datetime.date(2024, 1, 6)),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='date',
            field=models.DateField(default=datetime.date(2024, 1, 6)),
        ),
    ]
