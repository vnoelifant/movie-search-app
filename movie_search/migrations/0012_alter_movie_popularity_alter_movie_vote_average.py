# Generated by Django 4.2.4 on 2023-09-06 22:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movie_search", "0011_alter_genre_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="popularity",
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="vote_average",
            field=models.FloatField(default=0),
        ),
    ]
