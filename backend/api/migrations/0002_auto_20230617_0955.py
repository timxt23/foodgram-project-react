# Generated by Django 3.0.5 on 2023-06-17 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='ingredient',
            index=models.Index(fields=['name'], name='api_ingredi_name_ed215b_idx'),
        ),
    ]
