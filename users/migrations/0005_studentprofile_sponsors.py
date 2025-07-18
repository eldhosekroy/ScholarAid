# Generated by Django 5.2.3 on 2025-06-24 06:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_scholarship'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='sponsors',
            field=models.ManyToManyField(blank=True, limit_choices_to={'role': 'sponsor'}, related_name='students_sponsored', to=settings.AUTH_USER_MODEL),
        ),
    ]
