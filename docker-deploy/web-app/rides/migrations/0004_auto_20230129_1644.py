# Generated by Django 3.2.16 on 2023-01-29 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0001_initial'),
        ('rides', '0003_alter_ride_vehicle_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='drivers.driver'),
        ),
        migrations.AlterField(
            model_name='ride',
            name='special_request',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='ride',
            name='vehicle_type',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
