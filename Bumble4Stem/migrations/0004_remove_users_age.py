# Generated by Django 4.0.3 on 2024-02-26 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bumble4Stem', '0003_remove_users_phn_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='age',
        ),
    ]
