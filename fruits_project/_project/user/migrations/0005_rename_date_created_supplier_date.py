# Generated by Django 3.2.23 on 2024-01-04 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20240104_1601'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplier',
            old_name='date_created',
            new_name='date',
        ),
    ]