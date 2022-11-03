# Generated by Django 4.1.2 on 2022-11-03 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movie_search", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="genre",
            name="genres",
        ),
        migrations.AddField(
            model_name="genre",
            name="name",
            field=models.CharField(default="", max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="genre",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]