# Generated by Django 5.0.2 on 2025-05-15 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_category_description_ar_category_description_en_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='venue_ar',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='venue_en',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
