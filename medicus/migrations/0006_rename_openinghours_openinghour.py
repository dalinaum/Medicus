# Generated by Django 4.1.7 on 2023-05-05 16:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("medicus", "0005_openinghours"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="OpeningHours",
            new_name="OpeningHour",
        ),
    ]
