# Generated by Django 4.2 on 2023-05-07 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Emplois", "0008_alter_emploiscours_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="emploiscours",
            name="id",
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="horaire",
            name="HCours",
            field=models.CharField(max_length=50),
        ),
    ]
