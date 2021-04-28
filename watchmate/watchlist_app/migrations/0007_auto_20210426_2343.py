# Generated by Django 3.1.7 on 2021-04-26 23:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0006_auto_20210426_2333'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reviews',
            options={'verbose_name_plural': 'Watchlist Reviews'},
        ),
        migrations.AlterModelOptions(
            name='streamplatform',
            options={'verbose_name_plural': 'Stream Platforms'},
        ),
        migrations.AlterModelOptions(
            name='watchlist',
            options={'verbose_name_plural': 'Watchlists'},
        ),
        migrations.AlterField(
            model_name='reviews',
            name='rating',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)]),
        ),
    ]