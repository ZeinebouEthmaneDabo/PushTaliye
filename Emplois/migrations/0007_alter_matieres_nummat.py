# Generated by Django 4.2 on 2023-05-07 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Emplois", "0006_alter_professeurs_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="matieres",
            name="Nummat",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]