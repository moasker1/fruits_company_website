# Generated by Django 3.2.23 on 2024-01-07 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0028_container_main_total_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='container',
            name='main_total_count',
        ),
    ]
