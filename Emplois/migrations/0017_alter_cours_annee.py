# Generated by Django 4.1.7 on 2023-06-11 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Emplois', '0016_alter_emploiscours_annee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cours',
            name='annee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Emplois.anneeencours'),
        ),
    ]
