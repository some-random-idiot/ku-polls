# Generated by Django 3.2.6 on 2021-08-30 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='choices',
            new_name='votes',
        ),
    ]
