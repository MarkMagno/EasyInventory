# Generated by Django 5.1.3 on 2024-12-16 02:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkoutrequest',
            name='use_case',
            field=models.TextField(validators=[django.core.validators.RegexValidator('^[\\s\\S]{10,500}$', 'Use case must be between 10 and 500 characters.')]),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='asset_number',
            field=models.CharField(max_length=20, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9-]+$', 'Asset number must contain only letters, numbers, and hyphens.')]),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='model_number',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9-]+$', 'Model number must contain only letters, numbers, and hyphens.')]),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
    ]
