# Generated by Django 4.2.7 on 2024-01-08 04:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movie_search", "0004_alter_movie_tmdb_id_alter_tvseries_tmdb_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movierecommendation",
            name="tmdb_id",
            field=models.PositiveSmallIntegerField(default=0, unique=True),
        ),
        migrations.AlterField(
            model_name="tvseriesrecommendation",
            name="tmdb_id",
            field=models.PositiveSmallIntegerField(default=0, unique=True),
        ),
    ]
