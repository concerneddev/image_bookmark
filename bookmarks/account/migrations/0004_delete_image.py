# Generated by Django 4.1.12 on 2023-11-03 11:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0003_rename_images_image_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Image",
        ),
    ]
