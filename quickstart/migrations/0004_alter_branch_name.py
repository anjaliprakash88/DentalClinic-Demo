# Generated by Django 5.1.5 on 2025-01-27 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0003_pharmacy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
