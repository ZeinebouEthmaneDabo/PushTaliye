# Generated by Django 4.2 on 2023-05-01 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "Emplois",
            "0002_alter_emploiscours_cd_horaire_alter_emploiscours_mat_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="grades",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="horaire",
            name="HCours",
            field=models.TimeField(),
        ),
    ]
