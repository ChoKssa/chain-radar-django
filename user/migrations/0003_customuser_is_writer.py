# Generated by Django 5.1.7 on 2025-03-29 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_customuser_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_writer',
            field=models.BooleanField(default=False),
        ),
    ]
