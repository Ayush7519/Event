# Generated by Django 4.2 on 2024-03-15 09:15

from django.db import migrations, models
import emsadmin.models


class Migration(migrations.Migration):
    dependencies = [
        ("emsadmin", "0044_event_status_alter_sponser_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sponser",
            name="photo",
            field=models.ImageField(upload_to=emsadmin.models.category_image_dir_path),
        ),
    ]
