# Generated by Django 4.0.2 on 2022-03-13 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('electrovec', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bikes',
            new_name='Bike',
        ),
        migrations.RenameModel(
            old_name='Cars',
            new_name='Car',
        ),
        migrations.RenameModel(
            old_name='Scooters',
            new_name='Scooter',
        ),
    ]
