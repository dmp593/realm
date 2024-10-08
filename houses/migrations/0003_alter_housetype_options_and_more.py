# Generated by Django 5.0.7 on 2024-09-15 13:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0002_alter_housefile_options_alter_housefile_house'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='housetype',
            options={'ordering': ['parent__name', 'name'], 'verbose_name': 'house type', 'verbose_name_plural': 'houses types'},
        ),
        migrations.AddField(
            model_name='house',
            name='adapted_for_reduced_mobility',
            field=models.BooleanField(blank=True, null=True, verbose_name='is adapted for people with reduced mobility'),
        ),
        migrations.AddField(
            model_name='house',
            name='floor_level',
            field=models.IntegerField(blank=True, null=True, verbose_name='floor level'),
        ),
        migrations.AddField(
            model_name='house',
            name='garage_included_in_price',
            field=models.BooleanField(blank=True, null=True, verbose_name='garage included in price'),
        ),
        migrations.AddField(
            model_name='house',
            name='has_balcony',
            field=models.BooleanField(blank=True, null=True, verbose_name='has balcony'),
        ),
        migrations.AddField(
            model_name='house',
            name='has_garden',
            field=models.BooleanField(blank=True, null=True, verbose_name='has garden'),
        ),
        migrations.AddField(
            model_name='house',
            name='has_lift',
            field=models.BooleanField(blank=True, null=True, verbose_name='has lift'),
        ),
        migrations.AddField(
            model_name='house',
            name='has_pool',
            field=models.BooleanField(blank=True, null=True, verbose_name='has pool'),
        ),
        migrations.AddField(
            model_name='house',
            name='has_terrace',
            field=models.BooleanField(blank=True, null=True, verbose_name='has terrace'),
        ),
        migrations.AddField(
            model_name='housetype',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', related_query_name='child', to='houses.housetype', verbose_name='parent type'),
        ),
        migrations.AlterField(
            model_name='house',
            name='has_garage',
            field=models.BooleanField(blank=True, null=True, verbose_name='has garage'),
        ),
        migrations.CreateModel(
            name='CountryTax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_rate', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='tax rate')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='houses.country', verbose_name='country')),
            ],
            options={
                'verbose_name': 'country tax',
                'verbose_name_plural': 'country taxes',
                'ordering': ['country', 'tax_rate'],
            },
        ),
        migrations.CreateModel(
            name='PricingTier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lower_bound', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='lower bound')),
                ('upper_bound', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='upper bound')),
                ('gross_cost_in_euros', models.DecimalField(decimal_places=2, max_digits=9, null=True, verbose_name='gross cost in euros')),
                ('country_tax', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='houses.countrytax', verbose_name='country tax')),
            ],
            options={
                'verbose_name': 'pricing tier',
                'verbose_name_plural': 'pricing tiers',
                'ordering': ['lower_bound'],
            },
        ),
    ]
