# Generated by Django 5.1.4 on 2025-01-22 15:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookapp', '0006_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='room_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='bookapp.room'),
        ),
    ]
