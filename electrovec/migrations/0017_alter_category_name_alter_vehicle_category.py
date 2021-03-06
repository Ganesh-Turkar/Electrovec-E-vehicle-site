# Generated by Django 4.0.2 on 2022-05-17 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('electrovec', '0016_alter_vehicle_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(
                choices=[('Bike', 'Bike'), ('Scooter', 'Scooter'), ('Car', 'Car')], max_length=50),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='category',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='electrovec.category'),
        ),
    ]
