from cProfile import Profile
from datetime import date
import datetime
import os
from pdb import Pdb
import zipfile
from django import forms

from django.urls import reverse
from . models import DEPART, Matieres, Profil, Salles, Professeurs, EmploisCours, Horaire, Jours, Semestre,AnneeEnCours,Semaine,DateJour, Tarification
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .forms import CoursForm, ProfForm, matForm
from django .template import RequestContext
from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.core.paginator import Paginator
from cProfile import Profile
from django.shortcuts import render
from . models import Profil, Salles, Niveau
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.db.models import Q
from .helpers import send_forget_password_mail
from django.contrib.auth.models import User
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ProfForm
from .models import Professeurs
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


#singin
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def singin(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    if request.method == 'POST':
        username = request.POST['username'] 
        password = request.POST['password'] 
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/index') 
        else:
            msg = 'Error login'
            form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form, 'msg': msg})   
    else:
        form = AuthenticationForm() 
        return render(request, 'login.html', {'form' : form})

 
#singup
def singup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/listrespo')
    else:
        form = UserCreationForm()
    
    return render(request, 'singup.html', {'form': form})

#supprimer responsable
def delete_username(request, username):
    try:
        user = User.objects.get(username=username)
        user.delete()
        messages.success(request, f"Username '{username}' deleted successfully.")
    except User.DoesNotExist:
        messages.error(request, f"Username '{username}' does not exist.")
    return redirect('display_usernames')  # Redirect to the display_usernames view



#SINGOUT

def signout(request):
    logout(request)
    return redirect('/singin')

#FORGOTPASS
def forgotpass(request):
   
    try:
      if request.method == 'POST':
        email = request.POST['email']
        username = request.POST.get['username']

      if not User.objects.filter(username=username).first():
          messages.success(request, 'Not user found with this username')
    
          return render(request, 'forgot_password.html')
    
          user_obj=User.objects.get(username=username)
          token   = str(uuid.uuid())
          send_forget_password_mail(user_obj , token)
    except Exception as e:
            print(e)
    return render(request, 'forgotpass.html')


        



@login_required
def profiladmi(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            return redirect('profiladmi')
       
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'profiladmi.html', {'form': form})








# Create your views here.


def salle_list_pdf(request):
    # Create the HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="salle_list.pdf"'

    # Create the PDF object, using the response object as its "file"
    p = canvas.Canvas(response)

    # Add the salle list to the PDF
    salles = [...]  # Replace [...] with your actual salle list data
    y = 700  # Initial y position
    for salle in salles:
        p.drawString(100, y, salle['NomSalles'])
        p.drawString(200, y, salle['CapSal'])
        p.drawString(300, y, salle['Niv'])
        y -= 20  # Move to the next line

    # Close the PDF object
    p.showPage()
    p.save()

    return response



@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)


def home(request):
    nom_salles = request.GET.get('nom_salles', '')
    cap_sal = request.GET.get('cap_sal', '')
    niv = request.GET.get('niv', '')

    queryset = Salles.objects.all()

    if nom_salles:
        queryset = queryset.filter(NomSalles__icontains=nom_salles)
    if cap_sal:
        queryset = queryset.filter(CapSal__icontains=cap_sal)
    if niv:
        queryset = queryset.filter(Niv__icontains=niv)

    return render(request, 'salle.html', {'salles': queryset})



# functions du filiere
# Ajout du Salle

@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def add(request):
    if request.method == 'POST':
        nomSalles = request.POST.get('nom')
        capSal = request.POST.get('capacite')
        niv = request.POST.get('niveau')
        try:
            Salles.objects.create(NomSalles=nomSalles, CapSal=capSal, Niv=niv)
            messages.success(request, 'Ajouté avec succès.', extra_tags='success')
        except IntegrityError as e:
            messages.error(request, 'Duplication détectée.', extra_tags='danger')
        return redirect('add')  # Redirect to the addSalle.html page after processing the form

    return render(request, 'addSalle.html')

# Update Method

@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def update(request, nomSalles):
    salles = get_object_or_404(Salles, NomSalles=nomSalles)

    if request.method == "POST":
        capSal = request.POST.get("capacite")
        niv = request.POST.get("niveau")

        # Vérifier si les champs sont vides
        if capSal and niv:
            salles.CapSal = capSal
            salles.Niv = niv
            salles.save()
            messages.success(request, "Modifié avec succès")
        else:
            messages.error(request, "Veuillez remplir tous les champs")

    return render(request, "updateSalle.html", {'salles': salles})

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def BASE(request):
    return render(request, 'base.html')

@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def salle(request):
    return render(request, 'salle.html')

from django.db.models import Max
import plotly.graph_objects as go
from plotly.offline import plot


@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)

def index(request):
    if request.method == "POST":
        annee = request.POST.get("annee")
        request.session["annee_selectionnee"] = annee
        semestre = request.POST.get("Semestre")
        request.session["semestre_selectionne"] = semestre

    count = Salles.objects.count()
    countp = Professeurs.objects.count()
    countd = DEPART.objects.count()
    countf = Profil.objects.count()
    Annees = AnneeEnCours.objects.all()
    Semestres = Semestre.objects.values_list('type', flat=True).distinct()
    annee_selectionnee = request.session.get("annee_selectionnee")
    semestre_selectionne = request.session.get("semestre_selectionne")
    
    annee_max = AnneeEnCours.objects.aggregate(max_annee=Max('annee'))['max_annee']

    # Retrieve data for the graph
    data = Salles.objects.all()
    labels = [s.NomSalles for s in data]
    values = [s.CapSal for s in data]

    bar_color = 'rgb(7, 81, 181)'  # Specify the color of the bars

    fig = go.Figure(data=[go.Bar(
        x=labels,
        y=values,
        marker=dict(color=bar_color, line=dict(color='rgb(26, 35, 126)', width=1.5)),  # Apply color and border to the bars
        opacity=0.8,  # Set the opacity of the bars
        textposition='auto'  # Set the position of the value labels
    )])

    fig.update_layout(
        title='Salles Capacities',
        xaxis=dict(
            title='Nom Salles',
            title_font=dict(size=14),
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title='Capacities',
            title_font=dict(size=14),
            tickfont=dict(size=12)
        ),
        plot_bgcolor='white',
        font=dict(
            family='Arial',
            color='black',
            size=12
        ),
        width=500,  # Set the width of the graph
        height=400  # Set the height of the graph
    )

    plot_div = plot(fig, output_type='div')

    return render(request, 'index.html', {'count': count, 'countp': countp, 'countd': countd, 'countf': countf, 'Annees': Annees, 'Semestre': Semestres, 'annee_selectionnee': annee_selectionnee, 'semestre_selectionne': semestre_selectionne, 'annee_max': annee_max, 'plot_div': plot_div})

@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def prof(request):
    return render(request, 'prof.html')

# Supprimer Salle

@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def destroy(request, nomSalles):
    salle = Salles.objects.get(NomSalles=nomSalles)
    salle.delete()
    return redirect("/salle")


# functions du filiere
# Ajout du filiere
@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def addF(request):
    if request.method == 'POST':
        nbetu = request.POST.get('nb')
        libpr = request.POST.get('lib')
        codepr = request.POST.get('code')

        niveau = Niveau.objects.get(Noniv=request.POST.get('niv'))

        try:
            Profil.objects.create(
                NbEtudlns=nbetu,
                Niv=niveau,
                LibelleProfil=libpr,
                codeProfil=codepr
            )
            messages.success(request, 'Ajouté avec succès.')
        except IntegrityError as e:
            messages.error(request, 'Duplication détectée.', extra_tags='danger')  # Set the extra_tags to 'danger' for the desired style

        return redirect('addF')  # Redirect to the addFil.html page after processing the form

    niveaux = Niveau.objects.all()
    return render(request, 'addFil.html', {'niveaux': niveaux})





    # update Filiere

@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def updatefil(request, cdP):
    profil = get_object_or_404(Profil, codeProfil=cdP)

    if request.method == "POST":
        nbetu = request.POST["nb"]

        niv = request.POST["niv"]
        libpr = request.POST["lib"]

        # Vérifier si les champs sont vides
        if libpr and niv and nbetu:
            profil.LibelleProfil = libpr
            profil.Niv = niv
            profil.NbEtudlns = nbetu
            profil.save()
            messages.success(request, "Modifié avec succès")
        else:
            messages.error(request, "Veuillez remplir tous les champs")

    return render(request, "updateFil.html", {"profil": profil})


# delete Filiere


def deleteF(request, codeF):
    pr = Profil.objects.get(codeProfil=codeF)
    pr.delete()
    return redirect("/filiere")


def homeF(request):
    codeProfil = request.GET.get('codeProfil', '')
    LibelleProfil = request.GET.get('LibelleProfil', '')
    Niv__Noniv = request.GET.get('Niv__Noniv', '')  # Corrected parameter name
    NbEtudlns = request.GET.get('NbEtudlns', '')

    queryset = Profil.objects.all()

    if codeProfil:
        queryset = queryset.filter(codeProfil__icontains=codeProfil)
    if LibelleProfil:
        queryset = queryset.filter(LibelleProfil__icontains=LibelleProfil)
    if Niv__Noniv:  # Corrected field name
        queryset = queryset.filter(Niv__Noniv__icontains=Niv__Noniv)
    if NbEtudlns:
        queryset = queryset.filter(NbEtudlns__icontains=NbEtudlns)

    niveaux = Niveau.objects.all()

    context = {"profil": queryset, "niveaux": niveaux}

    return render(request, "filiere.html", context)



def liste_paginee(request):
    obj_list = Salles.objects.all() 
    paginator = Paginator(obj_list, 10)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, 'salle.html', context)






from django.shortcuts import get_object_or_404

@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def addM(request, filiere_id):
    profile = get_object_or_404(Profil, codeProfil=filiere_id)
    niveau = profile.Niv  # Récupérer le niveau de la filière
    Semestre_selectionnee =request.session.get("semestre_selectionne")
    semestres = Semestre.objects.filter(Niv=niveau,type=Semestre_selectionnee)  # Filtrer les semestres par le niveau de la filière

    if request.method == "POST":
        Nummat=request.POST.get("Num")
        mat = request.POST.get("mat")
        semestre_id = request.POST.get("sem")
        cm = int(request.POST.get("cm"))
        td = int(request.POST.get("td"))
        tp = int(request.POST.get("tp"))
        pr = int(request.POST.get("pr"))

        try:
            Sem = semestres.get(NSem=semestre_id)  # Récupérer le semestre correspondant à l'ID sélectionné
            Matieres.objects.create(
                Nummat=Nummat,
                Mat=mat,
                Noprfl=profile,
                Sem=Sem,
                CM=cm,
                TD=td,
                TP=tp,
                PR=pr
            )
            messages.success(request, "Matière ajoutée avec succès.", extra_tags='success')
        except IntegrityError as e:
            messages.error(request, "Duplication détectée.", extra_tags='danger')

        return redirect("addM", filiere_id=filiere_id)

    return render(request, "addmatiers.html", {"profil": profile, "semestres": semestres})




@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def addprof(request):
    if request.method == 'POST':
        form = ProfForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ajouté avec succès.', extra_tags='success')
            return redirect('/addp')
        else:
            messages.error(request, 'Erreur de validation du formulaire.', extra_tags='danger')
    else:
        form = ProfForm()
    return render(request, 'prof.html', {'form': form})



# update professeurs

@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def updateprof(request, matricule):
    prof = Professeurs.objects.get(Matricule=matricule)
    if request.method == 'POST':
        form = ProfForm(request.POST, instance=prof)
        if form.is_valid():
            # Exclure le champ "Matricule" lors de la sauvegarde du formulaire
            excluded_fields = ['Matricule']
            for field in excluded_fields:
                if field in form.cleaned_data:
                    del form.cleaned_data[field]
            form.save()
            return redirect('/Listeprof')
    else:
        # Exclure le champ "Matricule" lors de l'affichage du formulaire
        form = ProfForm(instance=prof)
        form.fields['Matricule'].widget.attrs['readonly'] = True  # Rendre le champ en lecture seule
    return render(request, 'updateProf.html', {'form': form})







# Affichage du


@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)

def homeP(request):
    no = request.GET.get('no', '')
    nom = request.GET.get('nom', '')
    sexe = request.GET.get('sexe', '')
    nodep = request.GET.get('nodep', '')
    type = request.GET.get('type', '')

    prof = Professeurs.objects.all()

    if no:
        prof = prof.filter(No__istartswith=no)
    if nom:
        prof = prof.filter(Nom__istartswith=nom)
    if sexe:
        prof = prof.filter(sexe__istartswith=sexe)
    if nodep:
        prof = prof.filter(Nodep__Nom__istartswith=nodep)
    if type:
        prof = prof.filter(Type__istartswith=type)

    return render(request, 'Listprof.html', {'professeurs': prof})





@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def deleteProf(request, matricule):
    prof = Professeurs.objects.get(Matricule=matricule)
    prof.delete()
    return redirect("/Listeprof")


from django.shortcuts import render, get_object_or_404
from .models import Profil, Matieres
@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def mat(request, filiere_id):
    semestre_selectionne = request.session.get("semestre_selectionne")
    filiere = get_object_or_404(Profil, codeProfil=filiere_id)
    search_query = request.GET.get('Mat', '')  # Get the value of the 'Mat' parameter from the query string
    matieres = Matieres.objects.filter(Noprfl=filiere_id, Sem__type=semestre_selectionne, Mat__icontains=search_query)
    context = {"Profil": filiere, "Matieres": matieres, "search_query": search_query}
    return render(request, "filiereProfil.html", context)


# update matiere


def updateMat(request,Nummat):
    matiere = get_object_or_404(Matieres, Nummat=Nummat)

    if request.method == "POST":
        mat = request.POST.get("mat")

        # Vérifier si le champ est vide
        if mat:
            matiere.Mat = mat
            matiere.save()
            messages.success(request, "Matière modifiée avec succès.")
            return redirect("updatemat", Nummat=Nummat)
        else:
            messages.error(request, "Veuillez remplir tous les champs.")

    return render(request, "updatemat.html", {"matiere": matiere})



# delete matiere


def deletem(request, nummat):
   
    prof = Matieres.objects.get(Nummat=nummat)
    filiere_id = prof.Noprfl.codeProfil 
    prof.delete()
    return redirect("/Listematiers/{0}".format(filiere_id))



def emp(request): 
    return render(request, 'affEmp.html')

def addc(request, filiere_id):
    profile = get_object_or_404(Profil, codeProfil=filiere_id)
    form = CoursForm(request.POST or None)
    Annees=AnneeEnCours.objects.all()
    annee_selectionnee = request.session.get("annee_selectionnee")  # Récupérer l'année depuis la variable de session
    annee_obj = AnneeEnCours.objects.get(annee=annee_selectionnee) 
    type_selectionne = request.session.get("semestre_selectionne")
    niveau_filiere = profile.Niv
    semestre = Semestre.objects.get(Niv=niveau_filiere,type=type_selectionne)

    derniere_annee = AnneeEnCours.objects.order_by('-annee').first()
    if request.method == "POST":
        if form.is_valid():
            cours = form.save(commit=False)
            cours.NOPRFL_id = filiere_id  # Assign the filiere_id to the foreign key
            cours.Semestre = semestre
            cours.annee= annee_obj
            matricule = form.cleaned_data.get("Matricule")
            cd_horaire = form.cleaned_data.get("Cd_Horaire")
            num_jour = form.cleaned_data.get("NumJour")
            
            salle = form.cleaned_data.get("salle")


            cours.save()
            return redirect("/affichCours/{0}".format(filiere_id)) 

    else:
      
      
        form.fields["Mat"].queryset = Matieres.objects.filter(Noprfl_id=filiere_id,Sem=semestre)
       

    context = {
        "form": form,
        "filiere_id": filiere_id,
        "Annees":Annees
}
    

    # Mettre à jour les options de sélection des salles et des professeurs
    if request.method == "POST" and form.is_valid():
        cd_horaire = form.cleaned_data["Cd_Horaire"]
        num_jour = form.cleaned_data["NumJour"]
        
        salles_occupees = EmploisCours.objects.filter(
            Cd_Horaire=cd_horaire, NumJour=num_jour,annee= annee_obj,Semestre__type=type_selectionne
        ).values_list('salle', flat=True)

        professeurs_occupees = EmploisCours.objects.filter(
            Cd_Horaire=cd_horaire, NumJour=num_jour,annee= annee_obj,Semestre__type=type_selectionne
        ).values_list('Matricule', flat=True)
        occupied_hours = EmploisCours.objects.filter(
           NumJour=num_jour,
           NOPRFL=profile,annee= annee_obj,Semestre__type=type_selectionne  # Ajoutez le filtrage par filière
       ).values_list('Cd_Horaire', flat=True)
        
        form.fields["Cd_Horaire"].queryset = Horaire.objects.all()
        form.fields["Cd_Horaire"].queryset = Horaire.exclude(cd__in=occupied_hours)
        form.fields["salle"].queryset = Salles.objects.exclude(id__in=salles_occupees)
        form.fields["Matricule"].queryset = Professeurs.objects.exclude(Matricule__in=professeurs_occupees)
        form.fields["salle"].queryset = Salles.objects.all()  # Liste complète des salles
        form.fields["Matricule"].queryset = Professeurs.objects.all()  # Liste complète des professeurs

    return render(request, "addc.html", context=context)
from django.http import JsonResponse




def occupancy_api(request):
    selected_jour = request.GET.get('jour')
    
    selected_horaire = request.GET.get('horaire')
    annee_selectionnee = request.session.get("annee_selectionnee")  # Récupérer l'année depuis la variable de session
    annee_obj = AnneeEnCours.objects.get(annee=annee_selectionnee) 
    type_selectionne = request.session.get("semestre_selectionne")
        # Récupération des salles et des professeurs occupés pour l'horaire et le jour spécifiés
    occupied_salles = EmploisCours.objects.filter(
            Cd_Horaire=selected_horaire,
            NumJour=selected_jour,annee= annee_obj,Semestre__type=type_selectionne
        ).values_list('salle', flat=True)

    occupied_professeurs = EmploisCours.objects.filter(
            Cd_Horaire=selected_horaire,
            NumJour=selected_jour,annee= annee_obj,Semestre__type=type_selectionne
        ).values_list('Matricule', flat=True)

    data = {
            'occupied_salles': list(occupied_salles),
            'occupied_professeurs': list(occupied_professeurs),
        }

    return JsonResponse(data)


def occupancyHeures_api(request):
    annee_selectionnee = request.session.get("annee_selectionnee")  # Récupérer l'année depuis la variable de session
    annee_obj = AnneeEnCours.objects.get(annee=annee_selectionnee) 
    type_selectionne = request.session.get("semestre_selectionne")
    selected_jour = request.GET.get('jour')
    filiere_id = request.GET.get('filiere_id')

    occupied_hours = EmploisCours.objects.filter(
        NumJour=selected_jour, NOPRFL=filiere_id,annee= annee_obj,Semestre__type=type_selectionne
    ).values_list('Cd_Horaire', flat=True)

    data = {
        
        'occupied_hours': list(occupied_hours),
        
    }

    return JsonResponse(data)

def homeC(request, filiere_id):
    filiere = get_object_or_404(Profil, codeProfil=filiere_id)
    annee_selectionnee = request.session.get("annee_selectionnee")  # Récupérer l'année depuis la variable de session
    annee_obj = AnneeEnCours.objects.get(annee=annee_selectionnee)  # Obtenir l'objet AnneeEnCours correspondant à l'année sélectionnée
    type_selectionne = request.session.get("semestre_selectionne")
    niveau_filiere = filiere.Niv
    semestre = Semestre.objects.get(Niv=niveau_filiere, type=type_selectionne)
    pr = EmploisCours.objects.filter(NOPRFL=filiere_id, annee=annee_obj.id,Semestre=semestre)  # Filtrer les emplois de cours par filière et ID de l'année
    context = {"Profil": filiere, "EmploisCours": pr, "AnneeSelectionnee": annee_obj}
    return render(request, "affichCours.html", context=context)


from django.http import JsonResponse


def updateCours(request, id):
    prof = EmploisCours.objects.get(id=id)
    if request.method == "POST":
        form = CoursForm(request.POST, instance=prof)
        if form.is_valid():
            form.save()
            return redirect("/Listeprof")
        else:
            context = {"form": form}
            return render(request, "updateCours.html", context=context, status=400)
    else:
        form = CoursForm(instance=prof)
        context = {"form": form}
        return render(request, "updateCours.html", context=context)


# delete cour

def deleteC(request, id):
    prof = EmploisCours.objects.get(id=id)
    filiere_id = prof.NOPRFL.codeProfil  # Récupérer l'ID de la filière
    prof.delete()
    return redirect("/affichCours/{0}".format(filiere_id))  # Redirection vers la page des cours avec l'ID de la filière




from django.shortcuts import render
from .models import EmploisCours


from datetime import date

def Emplois(request, code_profil):
    # Récupérer l'année en cours
    profil = get_object_or_404(Profil, codeProfil=code_profil)
    annee_selectionnee = request.session.get("annee_selectionnee")  # Récupérer l'année depuis la variable de session
    annee_obj = AnneeEnCours.objects.get(annee=annee_selectionnee) 
    derniere_annee = AnneeEnCours.objects.order_by('-annee').first()
    type_selectionne = request.session.get("semestre_selectionne")
    niveau_filiere = profil.Niv
    semestre = Semestre.objects.get(Niv=niveau_filiere, type=type_selectionne)
    Se=semestre.NSem
    anneec = annee_obj.annee if annee_obj else date.today().year
    # Calculer l'année précédente
    annee_precedente = anneec - 1

    # Récupérer le profil correspondant
  
    jours = Jours.objects.all()
    heures = Horaire.objects.all()

    c_j_h = []
    cours = EmploisCours.objects.filter(NOPRFL=profil,annee= annee_obj,Semestre=semestre)
    for cours_item in cours:
        if cours_item.Cd_Horaire in heures and cours_item.NumJour in jours:
            c_j_h.append((cours_item.Mat, cours_item.NumJour, cours_item.Cd_Horaire, cours_item.Matricule, cours_item.salle))

    context = {
        'c_j_h': c_j_h,
        'jours': jours,
        'heures': heures,
        'profil': profil,
        'annee_en_cours': anneec,
        'annee_precedente': annee_precedente,
        'semestre': Se
    }
    return render(request, 'Emplois.html', context)
def ListeEmplois(request):
    # Récupérer l'année en cours
    annee_selectionnee = request.session.get("annee_selectionnee")  # Récupérer l'année depuis la variable de session
    annee_obj = AnneeEnCours.objects.get(annee=annee_selectionnee) 
    derniere_annee = AnneeEnCours.objects.order_by('-annee').first()
    type_selectionne = request.session.get("semestre_selectionne")

    # Récupérer toutes les filières
    filieres = Profil.objects.all()
    se=[]
    c_j_h = []
    for filiere in filieres:
        niveau_filiere = filiere.Niv
        semestre = Semestre.objects.get(Niv=niveau_filiere,type=type_selectionne)
        Se = semestre.NSem
        anneec = annee_obj.annee if annee_obj else date.today().year
        # Calculer l'année précédente
        annee_precedente = anneec - 1
        
        jours = Jours.objects.all() 
        heures = Horaire.objects.all()
        # Récupérer tous les profils de la filière
        

        cours = EmploisCours.objects.filter(NOPRFL=filiere, annee=annee_obj, Semestre=semestre)
        for cours_item in cours:
            if cours_item.Cd_Horaire in heures and cours_item.NumJour in jours:
                    c_j_h.append((filiere, cours_item.Mat, cours_item.NumJour, cours_item.Cd_Horaire, cours_item.Matricule, cours_item.salle))
                    

    context = {
        'c_j_h': c_j_h,
        'jours': jours,
        'heures': heures,
        'filieres': filieres,
        'annee_en_cours': anneec,
        'annee_precedente': annee_precedente,
        'semestre': Se,
    }

    # Rendre la template pour afficher les emplois de toutes les filières
    return render(request, 'ListeEmplois.html', context)



def ListeEmpSalles(request):
    salles=Salles.objects.all()
    annee_selectionnee = request.session.get("annee_selectionnee")  # Récupérer l'année depuis la variable de session
    annee_obj = AnneeEnCours.objects.get(annee=annee_selectionnee) 
    derniere_annee = AnneeEnCours.objects.order_by('-annee').first()
 
    anneec = annee_obj.annee if annee_obj else date.today().year
  
    # Calculer l'année précédente
    annee_precedente = anneec - 1
    type_selectionne = request.session.get("semestre_selectionne")
    
    
    c_j_h = []
    for salle0 in salles:
     
        jours = Jours.objects.all()
        heures = Horaire.objects.all()
        semestres = Semestre.objects.filter(type=type_selectionne)
        semestre_list = [semestre.NSem for semestre in semestres]
        cours = EmploisCours.objects.filter(salle=salle0, annee=annee_obj, Semestre__type=type_selectionne)

        for cours_item in cours:
           if cours_item.Cd_Horaire in heures and cours_item.NumJour in jours:
             c_j_h.append((salle0, cours_item.Mat, cours_item.NumJour, cours_item.Cd_Horaire, cours_item.Matricule, cours_item.NOPRFL))

            
    context = {
        'c_j_h': c_j_h,
        'jours': jours,
        'heures': heures,
        'salles': salles,
        'annee_en_cours': anneec,
        'annee_precedente': annee_precedente,
        'semestre':semestre_list
    }
    return render(request, "ListeEmpSalles.html", context) 

def ListeEmpProfs(request):
    profs =Professeurs.objects.all()
    annee_selectionnee = request.session.get("annee_selectionnee")  # Récupérer l'année depuis la variable de session
    annee_obj = AnneeEnCours.objects.get(annee=annee_selectionnee) 
    derniere_annee = AnneeEnCours.objects.order_by('-annee').first()
    anneec = annee_obj.annee if annee_obj else date.today().year
    # Calculer l'année précédente
    annee_precedente = anneec - 1
    # Récupérer le profil correspondant
    type_selectionne = request.session.get("semestre_selectionne")
    c_j_h = []
    for prof in profs :
       jours = Jours.objects.all()
       heures = Horaire.objects.all()
       semestres = Semestre.objects.filter(type=type_selectionne)
       semestre_list = [semestre.NSem for semestre in semestres]
       cours = EmploisCours.objects.filter(Matricule=prof,annee=annee_obj,Semestre__type=type_selectionne)
       for cours_item in cours:
          if cours_item.Cd_Horaire in heures and cours_item.NumJour in jours:
             c_j_h.append((prof,cours_item.Mat, cours_item.NumJour, cours_item.Cd_Horaire, cours_item.salle, cours_item.NOPRFL))

    context = {
        'c_j_h': c_j_h,
        'jours': jours,
        'heures': heures,
        'Profs':  profs ,
        'annee_en_cours': anneec,
        'annee_precedente': annee_precedente,
        'semestre':semestre_list

    }
    return render(request, 'ListeEmpProfs.html', context)



# def ListeEmpSalles(request):
#     # Passer les données à la template
#     salles=Salles.objects.all()

#     context = {
#         "Salles": salles,
#     }

#     # Rendre la template pour afficher les emplois de la filière
#     return render(request, "ListeEmpSalles.html", context) 

from django.contrib.auth.models import User

def display_usernames(request):
    users = User.objects.all()  # Retrieve all user objects from the database
    return render(request, 'listrespo.html', {'users': users})



from django.http import JsonResponse
from .models import Salles

def get_salles(request):
    search_query = request.GET.get('search', '')

    salles = Salles.objects.filter(NomSalles__icontains=search_query)

    payload = [{'id': salle.NomSalles, 'salle': salle.NomSalles} for salle in salles]


    data = {
        'payload': payload
    }

    return JsonResponse(data)

from django.shortcuts import render
from datetime import timedelta

from django.shortcuts import render
from datetime import timedelta
from .models import Semaine, DateJour, Jours

from datetime import timedelta
from datetime import datetime, timedelta
from .models import Semaine, DateJour, Jours

from datetime import datetime, timedelta
from .models import Semaine, DateJour, Jours,TypeSemestre

def enregistrer_debut_semaines(request):
    if request.method == 'POST':
        # Récupérer la date de début à partir du formulaire
        date_debut = request.POST.get('date-debut')

        # Convertir la date de début en objet de type datetime
        date_debut = datetime.strptime(date_debut, '%Y-%m-%d')

        # Récupérer l'année et la parité sélectionnées dans la session
        annee = request.session.get('annee_selectionnee')
        parite = request.session.get('semestre_selectionne')
        annee_obj = AnneeEnCours.objects.get(annee=annee) 
        parite_obj=TypeSemestre.objects.get(parite=parite) 
        # Parcourir les 16 semaines
        for i in range(16):
            # Calculer la date du jour en ajoutant le numéro de semaine * 7 jours à la date de début
            date_jour = date_debut + timedelta(days=i * 7)

            # Calculer le numéro de la semaine
            numero_semaine = "S" + str(i + 1)
 
            # Créer une nouvelle instance de Semaine avec le numéro de semaine, l'année et la parité
            semaine = Semaine.objects.create(semaine=numero_semaine, annee=annee_obj, parite=parite_obj, gen=False)

            # Récupérer tous les jours de la semaine
            jours_semaine = Jours.objects.all()

           # Créer une nouvelle instance de DateJour pour chaque jour de la semaine
            for j, jour in enumerate(jours_semaine):
                # Calculer la date du jour en ajoutant j jours à la date de début de la semaine
                date_jour_semaine = date_jour + timedelta(days=j)

                # Formater la date du jour
                date_jour_str = date_jour_semaine.strftime('%Y-%m-%d')

                # Créer une instance de DateJour avec la semaine, le jour et la date correspondants
                date_jour_obj = DateJour(Semaine=semaine, NumJour=jour, DateJour=date_jour_str)

                # Sauvegarder l'instance dans la base de données
                date_jour_obj.save()

            # Calculer la date du jour suivant pour la prochaine itération
            date_jour += timedelta(days=1)

        # Afficher un message de succès ou rediriger vers une autre page
        return render(request, 'filiere.html')

    return render(request, 'DateJoursCreate.html')




from django.shortcuts import render
from .models import Semaine, Cours, DateJour

def affichCoursSemaine(request):
    annee_selectionnee = request.session.get("annee_selectionnee")  # Récupérer l'année depuis la variable de session
    parite = request.session.get('semestre_selectionne')
    annee_obj = AnneeEnCours.objects.get(annee=annee_selectionnee) 
    parite_obj=TypeSemestre.objects.get(parite=parite) 
    cours_semaine = Cours.objects.filter(semaine__gen=True)
    semaines = Semaine.objects.filter(gen=True,annee=annee_obj,parite=parite_obj)
    jours = Jours.objects.all()

    context = {
        'cours_semaine': cours_semaine,
        'jours': jours,
        'semaines': semaines
    }
    return render(request, 'affichCoursSemaine.html', context)

def generer_semaine(request):
    if request.method == 'POST':
        derniere_annee = AnneeEnCours.objects.order_by('-annee').first()
        annee_selectionnee = request.session.get("annee_selectionnee")  # Récupérer l'année depuis la variable de session
        parite = request.session.get('semestre_selectionne')
        annee_obj = AnneeEnCours.objects.get(annee=annee_selectionnee) 
        parite_obj=TypeSemestre.objects.get(parite=parite) 
        semaine_ids = request.POST.getlist('semaines')
        
        if not semaine_ids:
            message = "Veuillez sélectionner au moins une semaine."
            semaines = Semaine.objects.filter(gen=False,annee=annee_obj,parite=parite_obj)
            context = {'semaines': semaines, 'error_message': message}
            return render(request, 'afficher_semaines.html', context)
        
        semaines = Semaine.objects.filter(id__in=semaine_ids,annee=annee_obj,parite=parite_obj)
        semaines_precedentes_non_generees = Semaine.objects.filter(gen=False, id__lt=semaine_ids[0])
        
        if semaines_precedentes_non_generees.exists():
            message = "Veuillez d'abord générer les semaines précédentes."
            semaines = Semaine.objects.filter(gen=False,annee=annee_obj,parite=parite_obj)
            context = {'semaines': semaines, 'error_message': message}
            return render(request, 'afficher_semaines.html', context)
        
        for semaine in semaines:
            semaine.gen = True
            semaine.save()

        jours = Jours.objects.all()
        
        for jour in jours:
            date_jours = DateJour.objects.filter(Semaine__in=semaines, NumJour=jour)

            for date_jour in date_jours:
                emplois_cours = EmploisCours.objects.filter(NumJour=jour,annee=annee_obj.id,Semestre__type=parite)

                for emploi in emplois_cours:
                    cours_existant = Cours.objects.filter(
                        matricule=emploi.Matricule, 
                        noprfl=emploi.NOPRFL,
                        mat=emploi.Mat,
                        cd_horaire=emploi.Cd_Horaire,
                        salle=emploi.salle,
                        semaine=date_jour.Semaine,
                        CDDateJour=date_jour,
                        NumJour=jour,
                        natcours=emploi.NatCours,
                        annee=emploi.annee,
                        Semestre=emploi.Semestre
                    ).exists()

                    if not cours_existant:
                        cours = Cours(
                            matricule=emploi.Matricule,
                            noprfl=emploi.NOPRFL,
                            mat=emploi.Mat,
                            cd_horaire=emploi.Cd_Horaire,
                            salle=emploi.salle,
                            semaine=date_jour.Semaine,
                            CDDateJour=date_jour,
                            NumJour=jour,
                            natcours=emploi.NatCours,
                            annee=emploi.annee,
                            Semestre=emploi.Semestre
                        )
                        cours.save()

        cours_semaine = Cours.objects.filter(semaine__in=semaines)
        semaines = Semaine.objects.filter(gen=True,annee=annee_obj,parite=parite_obj)
        context = {
            'cours_semaine': cours_semaine,
            'jours': jours,
            'semaines': semaines
        }
        return render(request, 'affichCoursSemaine.html', context)
    annee_selectionnee = request.session.get("annee_selectionnee")  # Récupérer l'année depuis la variable de session
    parite = request.session.get('semestre_selectionne')
    annee_obj = AnneeEnCours.objects.get(annee=annee_selectionnee) 
    parite_obj=TypeSemestre.objects.get(parite=parite) 
    semaines = Semaine.objects.filter(gen=False,annee=annee_obj,parite=parite_obj)
    context = {'semaines': semaines}
    return render(request, 'afficher_semaines.html', context)


def liste_jours(request, semaine_id):
    annee_selectionnee = request.session.get("annee_selectionnee")  # Récupérer l'année depuis la variable de session
    annee_obj = AnneeEnCours.objects.get(annee=annee_selectionnee) 
    derniere_annee = AnneeEnCours.objects.order_by('-annee').first()
    anneec = annee_obj.annee if annee_obj else date.today().year
    parite = request.session.get('semestre_selectionne')
    matsoir_options = Horaire.objects.values_list('MatSoir', flat=True).distinct()

    # Calculer l'année précédente
    annee_precedente = anneec - 1
    semaine = Semaine.objects.get(id=semaine_id)
    jours = Jours.objects.all()
    context = {
        'semaine': semaine, 
        'jours': jours,
        'annee_en_cours': anneec,
        'annee_precedente': annee_precedente,
        'parite': parite,
        'matsoir_options': matsoir_options,
    }
    return render(request, 'liste_jours.html', context)

def afficher_cours_jour(request, semaine_id, jour_id, matSoir):

    semaine = Semaine.objects.get(id=semaine_id)
    jour = Jours.objects.get(NumJour=jour_id)
    cours_jour = Cours.objects.filter(semaine=semaine, NumJour=jour, cd_horaire__MatSoir=matSoir).order_by('cd_horaire')
    datei=DateJour.objects.get(Semaine=semaine,NumJour=jour)
    dat=datei.DateJour
    cours_html = ''
    cours_html += '<div class="hi">'
    cours_html += '<p class="helo">Date du jour : ' + str(dat) + '</p>'  # Add the DateJour paragraph
    cours_html += '</div>'
    if cours_jour:
        cours_html += '<div class="container">'
        
        cours_html += '<link rel="stylesheet" href="{% static \'assets/plugins/bootstrap/css/bootstrap.min.css\' %}">'
        cours_html += '<link rel="stylesheet" href="{% static \'assets/plugins/feather/feather.css\' %}">'
        cours_html += '<link rel="stylesheet" href="{% static \'assets/plugins/icons/flags/flags.css\' %}">'
        cours_html += '<link rel="stylesheet" href="{% static \'assets/plugins/fontawesome/css/fontawesome.min.css\' %}">'
        cours_html += '<link rel="stylesheet" href="{% static \'assets/plugins/fontawesome/css/all.min.css\' %}">'
        cours_html += '<link rel="stylesheet" href="{% static \'assets/plugins/select2/css/select2.min.css\' %}">'
        cours_html += '<link rel="stylesheet" href="{% static \'assets/css/style.css\' %}">'
        cours_html += '<script src="{% static \'assets/js/jquery-3.6.0.min.js\' %}"></script>'
        cours_html += '<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.4/css/jquery.dataTables.min.css">'
        cours_html += '<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.4/css/dataTables.bootstrap5.min.css">'
    
        cours_html += '<div class="table-responsive">'
        cours_html += '<table class="table" id="cours-table">'


        cours_html += '<thead>'
        cours_html += '<tr>' 
        cours_html += '<th>Filiere</th>'
        cours_html += '<th>Matiere</th>'
        cours_html += '<th>Professeur</th>'
        cours_html += '<th>Télé</th>'
        cours_html += '<th>Salle</th>'
        
        cours_html += '<th>Horaire</th>'
       
        cours_html += '<th>Date Jour</th>'
        cours_html += '<th>Signature</th>'
        cours_html += '</tr>'
        cours_html += '</thead>'
        cours_html += '<tbody>'
        for cours in cours_jour:
            cours_html += '<tr>'
            cours_html += '<td>' + str(cours.noprfl.LibelleProfil) + '</td>'
            cours_html += '<td> ' + str(cours.mat.Mat) + '</td>'
            cours_html += '<td> ' + str(cours.matricule.Nom) + '</td>'
            cours_html += '<td> ' + str(cours.matricule.Telephone) + '</td>'
            
            cours_html += '<td> ' + str(cours.salle.NomSalles) + '</td>'
            cours_html += '<td> ' + str(cours.cd_horaire.HCours) + '</td>'
            
            cours_html += '<td> ' + str(cours.CDDateJour.DateJour) + '</td>'
            cours_html += '<td>' + ('') + '</td>'


            cours_html += '</tr>'
           
        cours_html += '</tbody>'
        cours_html += '</table>'
    else:
      cours_html = '<p>Aucun cours disponible pour cette semaine et ce jour.</p>'
   
    return HttpResponse(cours_html)

def remplir_cours(request, semaine_id, jour_id,matSoir):
    semaine = Semaine.objects.get(id=semaine_id)
    jour = Jours.objects.get(NumJour=jour_id)
    cours = Cours.objects.filter(semaine=semaine,NumJour=jour,cd_horaire__MatSoir=matSoir)

    context = {'cours': cours}
    return render(request, 'remplir_cours.html', context)


import json
import json

def enregistrer_cours(request):
    if request.method == 'POST':
        cours_data = json.loads(request.POST.get('coursData'))

        for cours in cours_data:
            try:
                cours_obj = Cours.objects.get(ID=cours['id'])
                cours_obj.vl = cours['vl']
                cours_obj.save()
            except Cours.DoesNotExist:
                # Gérer le cas où aucun objet Cours correspondant à l'ID n'est trouvé
                pass

        return HttpResponse('Les cours ont été enregistrés avec succès !')


from django.shortcuts import render
from .models import Matieres, Cours

from django.shortcuts import render
from .models import Matieres, Cours
from django.db.models import Count




from django.http import JsonResponse

def matSuivie(request):
    annee_selectionnee = request.session.get("annee_selectionnee")  # Récupérer l'année depuis la variable de session
    type_selectionne = request.session.get('semestre_selectionne')
    annee_obj = AnneeEnCours.objects.get(annee=annee_selectionnee)
    anneec = annee_obj.annee if annee_obj else date.today().year
  
    # Calculer l'année précédente
    annee_precedente = anneec - 1 
    semestres = Semestre.objects.filter(type=type_selectionne)
    semestre_list = [semestre.NSem for semestre in semestres]
    matieres = Matieres.objects.filter(Sem__type=type_selectionne)
    filieres = Profil.objects.all()
    for matiere in matieres:
        matiere.planification = {
            'CM': Cours.objects.filter(mat=matiere, natcours='CM', vl=True,annee=annee_obj,Semestre__type=type_selectionne).count(),
            'TD': Cours.objects.filter(mat=matiere, natcours='TD', vl=True,annee=annee_obj,Semestre__type=type_selectionne).count(),
            'TP': Cours.objects.filter(mat=matiere, natcours='TP', vl=True,annee=annee_obj,Semestre__type=type_selectionne).count(),
            'PR': Cours.objects.filter(mat=matiere, natcours='PR', vl=True,annee=annee_obj,Semestre__type=type_selectionne).count()
        }

        matiere.realisation = {
            'TD': Cours.objects.filter(mat=matiere, natcours='TD', vl=True, annee=annee_obj,Semestre__type=type_selectionne).count(),      
            'CM': Cours.objects.filter(mat=matiere, natcours='CM', vl=True, annee=annee_obj,Semestre__type=type_selectionne).count(),
            'TP': Cours.objects.filter(mat=matiere, natcours='TP', vl=True, annee=annee_obj,Semestre__type=type_selectionne).count(),          
            'PR': Cours.objects.filter(mat=matiere, natcours='PR', vl=True, annee=annee_obj,Semestre__type=type_selectionne).count(),
        }

        matiere.avancement = {
            'CM': round((matiere.realisation['CM'] / matiere.CM) * 100, 2),
            'TD': round((matiere.realisation['TD'] / matiere.TD) * 100, 2),
            'TP': round((matiere.realisation['TP'] / matiere.TP) * 100, 2),
            'PR': round((matiere.realisation['PR'] / matiere.PR) * 100, 2)
        }

    context = {
        'Matieres': matieres,
        'filieres': filieres,
         'annee':annee_selectionnee,
         'annee_precedente':annee_precedente,
         'semestres':semestre_list

    }

    return render(request, 'Suivie_matieres.html', context)



def professeurs_table(request):
    professeurs = Professeurs.objects.all()
    annee_selectionnee = request.session.get("annee_selectionnee")  # Récupérer l'année depuis la variable de session
    type_selectionne = request.session.get('semestre_selectionne')
    annee_obj = AnneeEnCours.objects.get(annee=annee_selectionnee)
    anneec = annee_obj.annee if annee_obj else date.today().year
  
    # Calculer l'année précédente
    annee_precedente = anneec - 1 
    semestres = Semestre.objects.filter(type=type_selectionne)
    semestre_list = [semestre.NSem for semestre in semestres]
    matieres = Matieres.objects.filter(Sem__type=type_selectionne)
    data = []
    
    for professeur in professeurs:
        cm_count = Cours.objects.filter(matricule=professeur, vl=True, natcours='CM',annee=annee_obj,Semestre__type=type_selectionne).count()
        td_count = Cours.objects.filter(matricule=professeur, vl=True, natcours='TD',annee=annee_obj,Semestre__type=type_selectionne).count()
        tp_count = Cours.objects.filter(matricule=professeur, vl=True, natcours='TP',annee=annee_obj,Semestre__type=type_selectionne).count()
        pr_count = Cours.objects.filter(matricule=professeur, vl=True, natcours='PR',annee=annee_obj,Semestre__type=type_selectionne).count()
        
        matieres = Cours.objects.filter(matricule=professeur).values_list('mat__Mat', flat=True).distinct()
        matieres_list = list(matieres)
        
        data.append({
            'id':professeur.NNI,
            'nom': professeur.Nom,
            'compte_bancaire': professeur.CompteBancaire,
            'cm_count': cm_count,
            'td_count': td_count,
            'tp_count': tp_count,
            'pr_count': pr_count,
            'matieres': matieres_list,
            })
        context={
            'annee':annee_selectionnee,
            'annee_precedente':annee_precedente,
            'semestres':semestre_list}
    return render(request, 'professeurs_table.html', {'data': data,'context':context})

from django.shortcuts import render, get_object_or_404
from .models import Professeurs
from django.shortcuts import render, get_object_or_404
from .models import Professeurs

def professeur_detail(request, professeur_id):
    tarification = Tarification.objects.first() 
    professeur = get_object_or_404(Professeurs, NNI=professeur_id)
    annee_selectionnee = request.session.get("annee_selectionnee")  # Récupérer l'année depuis la variable de session
    type_selectionne = request.session.get('semestre_selectionne')
    annee_obj = AnneeEnCours.objects.get(annee=annee_selectionnee)
    anneec = annee_obj.annee if annee_obj else date.today().year
  
    # Calculer l'année précédente
    annee_precedente = anneec - 1 
    semestres = Semestre.objects.filter(type=type_selectionne)
    semestre_list = [semestre.NSem for semestre in semestres]
    matieres = Matieres.objects.filter(Sem__type=type_selectionne)
    # Get the selected date range from the request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    cm_count = Cours.objects.filter(matricule=professeur, vl=True, natcours='CM', annee=annee_obj, Semestre__type=type_selectionne)
    td_count = Cours.objects.filter(matricule=professeur, vl=True, natcours='TD', annee=annee_obj, Semestre__type=type_selectionne)
    tp_count = Cours.objects.filter(matricule=professeur, vl=True, natcours='TP', annee=annee_obj, Semestre__type=type_selectionne)
    pr_count = Cours.objects.filter(matricule=professeur, vl=True, natcours='PR', annee=annee_obj, Semestre__type=type_selectionne)
    
    # Filter the courses by the selected date range
    if start_date and end_date:
        cm_count = cm_count.filter(CDDateJour__DateJour__range=[start_date, end_date])
        td_count = td_count.filter(CDDateJour__DateJour__range=[start_date, end_date])
        tp_count = tp_count.filter(CDDateJour__DateJour__range=[start_date, end_date])
        pr_count = pr_count.filter(CDDateJour__DateJour__range=[start_date, end_date])

    cm_count = cm_count.count()
    td_count = td_count.count()
    tp_count = tp_count.count()
    pr_count = pr_count.count()
    total=cm_count+td_count +tp_count+pr_count 
    # calcul de prix
    prix_cm =  int(cm_count) * int(tarification.CM)
    prix_td = int(td_count) * int(tarification.TD)
    prix_tp =  int(tp_count) * int(tarification.TP)
    prix_pr = int( pr_count) * int(tarification.PR)

    totalPrix = prix_cm + prix_td+prix_tp+prix_pr
    matieres = Cours.objects.filter(matricule=professeur,vl=True,annee=annee_obj, Semestre__type=type_selectionne).values_list('mat__Mat', flat=True).distinct()
    matieres_list = list(matieres)

    data = {
        'nom': professeur.Nom,
        'compte_bancaire': professeur.CompteBancaire,
        'cm_count': cm_count,
        'td_count': td_count,
        'tp_count': tp_count,
        'pr_count': pr_count,
        'matieres': matieres_list,
        'total':total,
        'prix_cm':prix_cm,
        'prix_td':prix_td,
        'prix_tp':prix_tp,
        'prix_pr':prix_pr,
        'totalPrix':totalPrix
    }

    context = {
        'annee': annee_selectionnee,
        'annee_precedente': annee_precedente,
        'semestres': semestre_list,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'professeur_detail.html', {'data': data, 'context': context})

from django.shortcuts import render
from .models import AnneeEnCours



from .models import AnneeEnCours



from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.views import View
from .models import AnneeEnCours, EmploisCours

from django.shortcuts import render
from .models import AnneeEnCours

def annee_en_cours(request):
    # Récupérer la dernière année enregistrée
    derniere_annee = AnneeEnCours.objects.order_by('-annee').first()

    context = {
        'annee_en_cours': derniere_annee
    }

    return render(request, 'IncrementAnnees.html', context)


def incrementer_annee(request):
    # Récupérer la dernière année enregistrée
    derniere_annee = AnneeEnCours.objects.order_by('-annee').first()

    # Incrémenter l'année
    nouvelle_annee = derniere_annee.annee + 1

    # Créer une nouvelle instance de l'objet AnneeEnCours avec la nouvelle année
    nouvelle_instance = AnneeEnCours.objects.create(annee=nouvelle_annee)

    # Rediriger vers la vue de l'année en cours
    return redirect('annee_en_cours')



