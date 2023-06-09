# Generated by Django 4.1.7 on 2023-06-01 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Emplois', '0011_niveau_typecours_remove_professeurs_matricule_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnneeEnCours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annee', models.IntegerField(default=2023)),
            ],
        ),
        migrations.AddField(
            model_name='emploiscours',
            name='annee',
            field=models.ForeignKey(default=2023, on_delete=django.db.models.deletion.CASCADE, to='Emplois.anneeencours'),
        ),
    ]
