# Generated by Django 4.0.2 on 2022-03-22 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electrovec', '0011_remove_bike_id_remove_car_id_remove_scooter_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bike',
            name='b_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='b_id'),
        ),
        migrations.AlterField(
            model_name='car',
            name='c_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='c_id'),
        ),
    ]
