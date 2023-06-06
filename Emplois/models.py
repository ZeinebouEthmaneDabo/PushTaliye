from django.db import models

# from Emplois.models import Jours
# Create your models here.


class DEPART(models.Model):
    Nom = models.CharField(max_length=100)
    NODEP = models.CharField(max_length=100, primary_key=True)



def _str_(self):
    return self.Nom


class Niveau(models.Model):
    
    Noniv= models.CharField(max_length=20, primary_key=True)
 
class Semestre(models.Model):
    
    NSem= models.CharField(max_length=20, primary_key=True)
    Niv=models.ForeignKey(Niveau, on_delete=models.CASCADE)

class Grades(models.Model):
    nomGrade = models.CharField(max_length=20)
    id = models.AutoField(primary_key=True)


def _str_(self):
    return f"({self.nomGrade})"


class Horaire(models.Model):
    cd = models.AutoField(primary_key=True)
    HCours = models.CharField(max_length=50)
    NbHeure = models.IntegerField()
    MatSoir = models.CharField(max_length=100, default="Matin")


def _str_(self):
    return f"({self.HCours})"


class Jours(models.Model):
    NumJour = models.IntegerField(primary_key=True)
    NomJour = models.CharField(max_length=100)


def _str_(self):
    return self.NomJour


class Professeurs(models.Model):
    NNI = models.IntegerField(primary_key=True)
    Nom = models.CharField(max_length=200)
    Nodep = models.ForeignKey(DEPART, on_delete=models.CASCADE)
    Type = models.CharField(max_length=50)
    Telephone = models.IntegerField()
    Email = models.EmailField(max_length=200)
    sexe = models.TextField(max_length=50)
    Grade = models.ForeignKey(Grades, on_delete=models.CASCADE)


def _str_(self):
    return f"({self.Nom})"


def _str_(self):
    return f"({self.Grade})"


class Profil(models.Model):
    NbEtudlns = models.IntegerField()
    Niv=models.ForeignKey(Niveau, on_delete=models.CASCADE)
    LibelleProfil = models.CharField(max_length=200)
    codeProfil = models.CharField(max_length=50, primary_key=True)


def _str_(self):
    return f"({self.LibelleProfil})"


class Groupe(models.Model):
    LibelleGroupe = models.CharField(max_length=200)
    Noprfl = models.ForeignKey(Profil, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)


def _str_(self):
    return f"({self.LibelleGroupe})"


class Salles(models.Model):
    NomSalles = models.CharField(max_length=50, primary_key=True)
    CapSal = models.IntegerField()
    Niv = models.CharField(max_length=100)


def _str_(self):
    return f"({self.NomSalles})"


class Matieres(models.Model):
    Mat = models.CharField(max_length=200)
    Noprfl = models.ForeignKey(Profil, on_delete=models.CASCADE)
    Nummat = models.AutoField(primary_key=True)
    Sem = models.ForeignKey(Semestre, on_delete=models.CASCADE)

def _str_(self):
    return f"({self.Mat})"

class typeCours(models.Model):
    type = models.CharField(max_length=20,primary_key=True)
    

def _str_(self):
    return f"({self.type})"

class AnneeEnCours(models.Model):
    annee = models.IntegerField(default=2023)  # Valeur initiale de l'année

    @staticmethod
    def increment_annee():
        annee_obj = AnneeEnCours.objects.first()
        if annee_obj:
            annee_obj.annee += 1
            annee_obj.save()
        else:
            AnneeEnCours.objects.create(annee=2023)  # Crée un nouvel objet si aucun n'existe

class EmploisCours(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    Matricule = models.ForeignKey(Professeurs, on_delete=models.CASCADE)
    NOPRFL = models.ForeignKey(Profil, on_delete=models.CASCADE)
    Mat = models.ForeignKey(Matieres, on_delete=models.CASCADE)
    Cd_Horaire = models.ForeignKey(Horaire, on_delete=models.CASCADE)
    salle = models.ForeignKey(Salles, on_delete=models.CASCADE)
    NumJour = models.ForeignKey(Jours, on_delete=models.CASCADE)
    NatCours = models.ForeignKey(typeCours, on_delete=models.CASCADE)
    annee = models.ForeignKey(AnneeEnCours, on_delete=models.CASCADE, default=2023)  # Lien avec le modèle AnneeEnCours
  


class Pgmemptemps(models.Model):
    Noprfl = models.ForeignKey(Profil, on_delete=models.CASCADE)
    Cd_Horaire = models.ForeignKey(Horaire, on_delete=models.CASCADE)
    J1 = models.CharField(max_length=500)
    J2 = models.CharField(max_length=500)
    J3 = models.CharField(max_length=500)
    J4 = models.CharField(max_length=500)
    J5 = models.CharField(max_length=500)
    J6 = models.CharField(max_length=500)


class PgmemptempsPr(models.Model):
    Matricule = models.ForeignKey(Professeurs, on_delete=models.CASCADE)
    Cd_Horaire = models.ForeignKey(Horaire, on_delete=models.CASCADE)
    J1 = models.CharField(max_length=500)
    J2 = models.CharField(max_length=500)
    J3 = models.CharField(max_length=500)
    J4 = models.CharField(max_length=500)
    J5 = models.CharField(max_length=500)
    J6 = models.CharField(max_length=500)


class PgmemptempsSI(models.Model):
    salle = models.ForeignKey(Salles, on_delete=models.CASCADE)
    Cd_Horaire = models.ForeignKey(Horaire, on_delete=models.CASCADE)
    J1 = models.CharField(max_length=500)
    J2 = models.CharField(max_length=500)
    J3 = models.CharField(max_length=500)
    J4 = models.CharField(max_length=500)
    J5 = models.CharField(max_length=500)
    J6 = models.CharField(max_length=500)


# Partie Suivi


# class Semaine(models.Model):
#     semaine=models.CharField(max_length=50)
#     gen=models.BooleanField(default=False)


# class DateJour(models.Model):
#     CDDateJour=models.IntegerField(primary_key=True)
#     Semaine=models.CharField(max_length=50)
#     NumJour=models.IntegerField()
#     DateJour=models.DateField()


# class Cours(models.Model):
#     ID=models.IntegerField(primary_key=True)  
#     matricule=models.CharField(max_length=50)
#     noprfl=models.CharField(max_length=50)
#     mat=models.CharField(max_length=50)
#     cd_horaire=models.IntegerField()
#     salle=models.CharField(max_length=50)
#     semaine=models.CharField(max_length=50)
#     CDDateJour=models.IntegerField()
#     DateJour=models.DateField()
#     vl=models.BooleanField(default=False)
#     NumJour=models.IntegerField()
#     natcours=models.CharField(max_length=50)