# Generated by Django 5.0.4 on 2024-05-26 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergames',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
