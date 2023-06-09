# Generated by Django 4.1.7 on 2023-05-04 18:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("medicus", "0002_medicalspecialty"),
    ]

    operations = [
        migrations.CreateModel(
            name="Doctor",
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
                ("name", models.CharField(max_length=50)),
                ("office_name", models.CharField(max_length=50)),
                ("specialties", models.ManyToManyField(to="medicus.medicalspecialty")),
            ],
        ),
    ]
