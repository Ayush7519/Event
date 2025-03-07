# Generated by Django 4.2 on 2024-03-22 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("content_management", "0007_comment_like_alter_comment_blog"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="blog",
        ),
        migrations.AddField(
            model_name="comment",
            name="blog",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="content_management.blog",
            ),
        ),
    ]
