# Generated by Django 5.0.7 on 2024-07-28 14:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0003_house_adapted_for_reduced_mobility_house_floor_level_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryTax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_rate', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='tax rate')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='houses.country', verbose_name='country')),
            ],
        ),
        migrations.CreateModel(
            name='PricingTier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lower_bound', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='lower bound')),
                ('upper_bound', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='upper bound')),
                ('gross_cost_in_euros', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='gross cost in euros')),
                ('country_tax', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='houses.countrytax', verbose_name='country tax')),
            ],
            options={
                'verbose_name': 'pricing tier',
                'verbose_name_plural': 'pricing tiers',
                'ordering': ['gross_cost_in_euros'],
            },
        ),
    ]
