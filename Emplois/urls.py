from django.urls import path
from . import views


urlpatterns = [
    
    path('BASE', views.BASE, name='BASE'),
    path('profiladmi', views.profiladmi, name='profiladmi'),
    path('index', views.index, name='index'),
    path('add', views.add, name='add'),
    path('listrespo', views.display_usernames, name='display_usernames'),
    path('listrespo/delete/<str:username>/', views.delete_username, name='delete_username'),
    path('', views.singin, name='singin'),
    path('singin', views.singin, name='singin'),
    path('singup', views.singup, name='singup'),
    path('signout', views.signout, name='signout'),
    path('forgotpass/', views.forgotpass, name='forgotpass'),
    path('addFil', views.addF, name='addF'),
    path('addm/<slug:filiere_id>', views.addM, name='addM'),
    path('addp', views.addprof, name='addp'),
    path('matSuivie/', views.matSuivie, name='matSuivie'),
    path('salle', views.home, name='salle'),
    path('filiere', views.homeF, name='filiere'),
    path('ListeEmplois', views.ListeEmplois, name='ListeEmplois'),
    path('Emplois/<slug:code_profil>', views.Emplois, name='Emplois'),
    path('ListeEmpSalles', views.ListeEmpSalles, name='ListeEmpSalles'),
    path('ListeEmpProfs', views.ListeEmpProfs, name='ListeEmpProfs'),
    path('professeurs/', views.professeurs_table, name='professeurs'),
    path('professeurs_table/<int:professeur_id>/', views.professeur_detail, name='professeur_detail'),

    path('affemp', views.emp, name='affEmp'),
    path("affichCours/<slug:filiere_id>", views.homeC, name="Cours"),
    path("cours/<slug:filiere_id>", views.addc, name="addc"), 
    path('Listeprof', views.homeP, name='prof'),
     
    path('Listematiers/<slug:filiere_id>', views.mat, name='mat'),
    path('delete/<slug:nomSalles>', views.destroy, name='delete'),
    path('updateS/<slug:nomSalles>', views.update, name='updateS'),
    path('updateFil/<slug:cdP>', views.updatefil, name='updateFil'),
    path('updateMat/<str:Nummat>', views.updateMat, name='updateMat'),
    path('updateCours/<slug:id>', views.updateCours, name='updateCours'),
    path('updateProf/<slug:nni>', views.updateprof, name='updateP'),
    path('deleteF/<slug:codeF>', views.deleteF, name='deleteF'),
    path("deleteC/<slug:id>", views.deleteC, name="deleteC"),
    path('deleteProf/<slug:matricule>', views.deleteProf, name='deleteP'),
    path('deletem/<slug:nummat>', views.deletem, name='deletem'),
    path('get_salles/', views.get_salles, name='get_salles'),
    path('api/occupancyHeures/', views.occupancyHeures_api, name='occupancyHeures'),
    path('api/occupancy/', views.occupancy_api, name='occupancy_api'),
    path('enregistrer_debut_semaines/', views.enregistrer_debut_semaines, name='enregistrer_debut_semaines'),
    path('generer_semaine/', views.generer_semaine, name='generer_semaine'),
    path('liste_jours/<int:semaine_id>/', views.liste_jours, name='liste_jours'),
    path('api/afficher_cours_jour/<int:semaine_id>/<int:jour_id>/<slug:matSoir>/', views.afficher_cours_jour, name='afficher_cours_jour'),

    path('remplir_cours/<int:semaine_id>/<int:jour_id>/<slug:matSoir>/', views.remplir_cours, name='remplir_cours'),
    path('enregistrer_cours/', views.enregistrer_cours, name='enregistrer_cours'),
    path('afficher_cours_semaine/', views.affichCoursSemaine, name='affichCoursSemaine'),
    path('annee-en-cours/', views.annee_en_cours, name='annee_en_cours'),
    path('incrementer-annee/', views.incrementer_annee, name='incrementer_annee'),
    

]