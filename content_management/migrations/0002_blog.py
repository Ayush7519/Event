# Generated by Django 4.2 on 2024-03-14 10:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("content_management", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("created_by", models.CharField(max_length=50, null=True)),
            ],
        ),
    ]
