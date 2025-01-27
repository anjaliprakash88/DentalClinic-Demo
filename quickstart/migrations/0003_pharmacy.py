# Generated by Django 5.1.5 on 2025-01-27 06:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0002_branch_doctor_branch'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pharmacy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience_years', models.PositiveIntegerField()),
                ('qualification', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pharmacys', to='quickstart.branch')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pharmacy', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
