# Generated by Django 5.0.4 on 2024-05-29 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_usergames_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergames',
            name='status',
            field=models.CharField(choices=[('playing', 'Playing'), ('will_play', 'Will Play'), ('finished', 'Finished')], max_length=10),
        ),
    ]
