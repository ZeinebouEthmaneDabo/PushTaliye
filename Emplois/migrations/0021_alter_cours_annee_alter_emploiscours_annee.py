# Generated by Django 4.1.7 on 2023-06-16 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Emplois', '0020_alter_cours_annee_alter_emploiscours_annee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cours',
            name='annee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Emplois.anneeencours'),
        ),
        migrations.AlterField(
            model_name='emploiscours',
            name='annee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Emplois.anneeencours'),
        ),
    ]
