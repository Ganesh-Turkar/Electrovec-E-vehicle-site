# Generated by Django 4.0.2 on 2022-05-26 11:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('electrovec', '0035_alter_userdetails_name_alter_userdetails_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
