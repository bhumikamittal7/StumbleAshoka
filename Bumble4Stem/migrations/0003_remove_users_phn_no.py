# Generated by Django 4.0.3 on 2024-02-14 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bumble4Stem', '0002_alter_users_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='phn_no',
        ),
    ]
