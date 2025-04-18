# Generated by Django 5.1.7 on 2025-03-30 16:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoCurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=10)),
                ('description', models.TextField(blank=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='crypto_logos/')),
            ],
        ),
        migrations.CreateModel(
            name='CryptoSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('price', models.DecimalField(decimal_places=8, max_digits=20)),
                ('market_cap', models.BigIntegerField()),
                ('volume_24h', models.BigIntegerField()),
                ('change_24h', models.FloatField(help_text='Pourcentage de variation sur 24h')),
                ('crypto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snapshots', to='crypto.cryptocurrency')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
