# Generated by Django 3.2 on 2024-07-15 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_auto_20240715_2042'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todotask',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='todotask',
            old_name='modified',
            new_name='modified_at',
        ),
    ]
