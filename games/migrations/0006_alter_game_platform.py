# Generated by Django 5.0.4 on 2024-05-29 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_game_average_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='platform',
            field=models.CharField(blank=True, choices=[('PC', 'PC'), ('Playstation', 'Playstation'), ('Xbox', 'Xbox'), ('Mobile', 'Mobile')], max_length=50, null=True),
        ),
    ]