# Generated by Django 5.1.5 on 2025-01-29 09:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0006_remove_pharmacy_branch'),
    ]

    operations = [
        migrations.AddField(
            model_name='pharmacy',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='pharmacys', to='quickstart.branch'),
            preserve_default=False,
        ),
    ]
