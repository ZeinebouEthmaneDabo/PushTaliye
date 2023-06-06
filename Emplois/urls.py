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
    path('salle', views.home, name='salle'),
    path('filiere', views.homeF, name='filiere'),
    path('ListeEmplois', views.ListeEmplois, name='ListeEmplois'),
    path('Emplois/<slug:code_profil>', views.Emplois, name='Emplois'),
    path('affemp', views.emp, name='affEmp'),
    path("affichCours/<slug:filiere_id>", views.homeC, name="Cours"),
    path("cours/<slug:filiere_id>", views.addc, name="addc"), 
    path('Listeprof', views.homeP, name='prof'),
     
    path('Listematiers/<slug:filiere_id>', views.mat, name='mat'),
    path('delete/<slug:nomSalles>', views.destroy, name='delete'),
    path('updateS/<slug:nomSalles>', views.update, name='updateS'),
    path('updateFil/<slug:cdP>', views.updatefil, name='updateFil'),
    path('updatemat/<slug:Nummat>', views.updatemat, name='updatemat'),
    path('updateCours/<slug:id>', views.updateCours, name='updateCours'),
    path('updateProf/<slug:matricule>', views.updateprof, name='updateP'),
    path('deleteF/<slug:codeF>', views.deleteF, name='deleteF'),
    path("deleteC/<slug:id>", views.deleteC, name="deleteC"),
    path('deleteProf/<slug:matricule>', views.deleteProf, name='deleteP'),
    path('deletem/<slug:nummat>', views.deletem, name='deletem'),
    path('export_to_pdf/<slug:code_profil>', views.export_to_pdf, name='export_to_pdf'),
    path('export_to_pdfCollectif', views.export_to_pdfCollectif, name='export_to_pdfCollectif'),
    path('get_salles/', views.get_salles, name='get_salles'),
    path('api/occupancy/', views.occupancy_api, name='occupancy_api'),
]
   

