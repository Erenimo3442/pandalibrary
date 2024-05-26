# Generated by Django 5.0.4 on 2024-05-26 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_alter_game_cover_alter_game_platform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='covers'),
        ),
        migrations.AlterField(
            model_name='game',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]