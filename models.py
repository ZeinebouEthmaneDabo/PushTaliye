# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models





class EmploisDepart(models.Model):
    # Field name made lowercase.
    nom = models.CharField(db_column='Nom', max_length=100)
    # Field name made lowercase.
    nodep = models.CharField(
        db_column='NODEP', primary_key=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'Emplois_depart'


class EmploisEmploiscours(models.Model):
    id = models.IntegerField(primary_key=True)
    # Field name made lowercase.
    natcours = models.CharField(db_column='NatCours', max_length=50)
    # Field name made lowercase.
    cd_horaire = models.ForeignKey(
        'EmploisHoraire', models.DO_NOTHING, db_column='Cd_Horaire_id')
    # Field name made lowercase.
    mat = models.ForeignKey(
        'EmploisMatieres', models.DO_NOTHING, db_column='Mat_id')
    # Field name made lowercase.
    matricule = models.ForeignKey(
        'EmploisProfesseurs', models.DO_NOTHING, db_column='Matricule_id')
    # Field name made lowercase.
    noprfl = models.ForeignKey(
        'EmploisProfil', models.DO_NOTHING, db_column='NOPRFL_id')
    # Field name made lowercase.
    numjour = models.ForeignKey(
        'EmploisJours', models.DO_NOTHING, db_column='NumJour_id')
    salle = models.ForeignKey('EmploisSalles', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Emplois_emploiscours'


class EmploisGrades(models.Model):
    # Field name made lowercase.
    nomgrade = models.CharField(db_column='nomGrade', max_length=20)
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'Emplois_grades'


class EmploisHoraire(models.Model):
    cd = models.AutoField(primary_key=True)
    # Field name made lowercase.
    hcours = models.IntegerField(db_column='HCours')
    # Field name made lowercase.
    nbheure = models.IntegerField(db_column='NbHeure')
    # Field name made lowercase.
    niv = models.CharField(db_column='Niv', max_length=100)
    # Field name made lowercase.
    matsoi = models.CharField(db_column='MatSoi', max_length=100)

    class Meta:
        managed = False
        db_table = 'Emplois_horaire'


class EmploisJours(models.Model):
    # Field name made lowercase.
    numjour = models.IntegerField(db_column='NumJour', primary_key=True)
    # Field name made lowercase.
    nomjour = models.CharField(db_column='NomJour', max_length=100)

    class Meta:
        managed = False
        db_table = 'Emplois_jours'


class EmploisMatieres(models.Model):
    # Field name made lowercase.
    mat = models.CharField(db_column='Mat', max_length=200)
    # Field name made lowercase.
    nummat = models.IntegerField(db_column='Nummat', primary_key=True)
    # Field name made lowercase.
    noprfl = models.ForeignKey(
        'EmploisProfil', models.DO_NOTHING, db_column='Noprfl_id')

    class Meta:
        managed = False
        db_table = 'Emplois_matieres'


class EmploisPgmemptemps(models.Model):
    id = models.BigAutoField(primary_key=True)
    # Field name made lowercase.
    j1 = models.CharField(db_column='J1', max_length=500)
    # Field name made lowercase.
    j2 = models.CharField(db_column='J2', max_length=500)
    # Field name made lowercase.
    j3 = models.CharField(db_column='J3', max_length=500)
    # Field name made lowercase.
    j4 = models.CharField(db_column='J4', max_length=500)
    # Field name made lowercase.
    j5 = models.CharField(db_column='J5', max_length=500)
    # Field name made lowercase.
    j6 = models.CharField(db_column='J6', max_length=500)
    # Field name made lowercase.
    cd_horaire = models.ForeignKey(
        EmploisHoraire, models.DO_NOTHING, db_column='Cd_Horaire_id')
    # Field name made lowercase.
    noprfl = models.ForeignKey(
        'EmploisProfil', models.DO_NOTHING, db_column='Noprfl_id')

    class Meta:
        managed = False
        db_table = 'Emplois_pgmemptemps'


class EmploisPgmemptempspr(models.Model):
    id = models.BigAutoField(primary_key=True)
    # Field name made lowercase.
    j1 = models.CharField(db_column='J1', max_length=500)
    # Field name made lowercase.
    j2 = models.CharField(db_column='J2', max_length=500)
    # Field name made lowercase.
    j3 = models.CharField(db_column='J3', max_length=500)
    # Field name made lowercase.
    j4 = models.CharField(db_column='J4', max_length=500)
    # Field name made lowercase.
    j5 = models.CharField(db_column='J5', max_length=500)
    # Field name made lowercase.
    j6 = models.CharField(db_column='J6', max_length=500)
    # Field name made lowercase.
    cd_horaire = models.ForeignKey(
        EmploisHoraire, models.DO_NOTHING, db_column='Cd_Horaire_id')
    # Field name made lowercase.
    matricule = models.ForeignKey(
        'EmploisProfesseurs', models.DO_NOTHING, db_column='Matricule_id')

    class Meta:
        managed = False
        db_table = 'Emplois_pgmemptempspr'


class EmploisPgmemptempssi(models.Model):
    id = models.BigAutoField(primary_key=True)
    # Field name made lowercase.
    j1 = models.CharField(db_column='J1', max_length=500)
    # Field name made lowercase.
    j2 = models.CharField(db_column='J2', max_length=500)
    # Field name made lowercase.
    j3 = models.CharField(db_column='J3', max_length=500)
    # Field name made lowercase.
    j4 = models.CharField(db_column='J4', max_length=500)
    # Field name made lowercase.
    j5 = models.CharField(db_column='J5', max_length=500)
    # Field name made lowercase.
    j6 = models.CharField(db_column='J6', max_length=500)
    # Field name made lowercase.
    cd_horaire = models.ForeignKey(
        EmploisHoraire, models.DO_NOTHING, db_column='Cd_Horaire_id')
    salle = models.ForeignKey('EmploisSalles', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Emplois_pgmemptempssi'


class EmploisProfesseurs(models.Model):
    # Field name made lowercase.
    matricule = models.CharField(
        db_column='Matricule', primary_key=True, max_length=50)
    # Field name made lowercase.
    nom = models.CharField(db_column='Nom', max_length=200)
    # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=50)
    # Field name made lowercase.
    telephone = models.IntegerField(db_column='Telephone')
    # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=200)
    sexe = models.TextField()
    # Field name made lowercase.
    grade = models.ForeignKey(
        EmploisGrades, models.DO_NOTHING, db_column='Grade_id')
    # Field name made lowercase.
    nodep = models.ForeignKey(
        EmploisDepart, models.DO_NOTHING, db_column='Nodep_id')

    class Meta:
        managed = False
        db_table = 'Emplois_professeurs'


class EmploisProfil(models.Model):
    # Field name made lowercase.
    nbetudlns = models.IntegerField(db_column='NbEtudlns')
    # Field name made lowercase.
    semestre = models.CharField(db_column='Semestre', max_length=50)
    # Field name made lowercase.
    niv = models.CharField(db_column='Niv', max_length=100)
    # Field name made lowercase.
    libelleprofil = models.CharField(db_column='LibelleProfil', max_length=200)
    # Field name made lowercase.
    codeprofil = models.CharField(
        db_column='codeProfil', primary_key=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'Emplois_profil'


class EmploisSalles(models.Model):
    # Field name made lowercase.
    nomsalles = models.CharField(
        db_column='NomSalles', primary_key=True, max_length=50)
    # Field name made lowercase.
    capsal = models.IntegerField(db_column='CapSal')
    # Field name made lowercase.
    niv = models.CharField(db_column='Niv', max_length=100)

    class Meta:
        managed = False
        db_table = 'Emplois_salles'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        'DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
