# Generated by Django 4.0.2 on 2022-05-17 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electrovec', '0025_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
