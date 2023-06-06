from cProfile import Profile
from datetime import date
from pdb import Pdb
import zipfile

from django.urls import reverse
from . models import DEPART, Matieres, Profil, Salles, Professeurs, EmploisCours, Horaire, Jours, Semestre,AnneeEnCours
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
    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(NomSalles__icontains=q) | Q(CapSal__icontains=q) | Q(Niv__icontains=q))
        salles = Salles.objects.filter(multiple_q)
    else:   
      salles = Salles.objects.all()
    return render(request, 'salle.html', {'salles': salles})

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


@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def index(request):
    count = Salles.objects.count()
    countp = Professeurs.objects.count()
    countd = DEPART.objects.count()
    countf = Profil.objects.count()
    return render(request, 'index.html', {'count': count, 'countp': countp, 'countd': countd, 'countf': countf })









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
    niveaux = Niveau.objects.all()

    if "q" in request.GET:
        niveau_id = request.GET["q"]
        if niveau_id:
            pr = Profil.objects.filter(Niv_id=niveau_id)
        else:
            pr = Profil.objects.all()
    else:
        pr = Profil.objects.all()

    context = {"profil": pr, "niveaux": niveaux}

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
    semestres = Semestre.objects.filter(Niv=niveau)  # Filtrer les semestres par le niveau de la filière

    if request.method == "POST":
        mat = request.POST.get("mat")
        semestre_id = request.POST.get("sem")
        try:
            Sem = semestres.get(NSem=semestre_id)  # Récupérer le semestre correspondant à l'ID sélectionné
            Matieres.objects.create(Mat=mat, Noprfl=profile, Sem=Sem)
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
    if 'q' in request.GET:
        q = request.GET['q']
        prof = Professeurs.objects.filter(
            Q(NNI__icontains=q) |
            Q(Nom__icontains=q) |
            Q(Nodep__Nom__icontains=q) |
            Q(Type__icontains=q) |
            Q(Telephone__icontains=q) |
            Q(Email__icontains=q) |
            Q(sexe__icontains=q) |
            Q(Grade__nomGrade__icontains=q)
        )
    else:   
        prof = Professeurs.objects.all()
    return render(request, 'Listprof.html', {'professeurs': prof})


@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def deleteProf(request, matricule):
    prof = Professeurs.objects.get(Matricule=matricule)
    prof.delete()
    return redirect("/Listeprof")

@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def mat(request, filiere_id):
    filiere = get_object_or_404(Profil, codeProfil=filiere_id)
    matieres = Matieres.objects.filter(Noprfl=filiere_id)
    context = {"Profil": filiere, "Matieres": matieres}
    return render(request, "filiereProfil.html", context)


# update matiere


def updatemat(request, Nummat):
    matiere = get_object_or_404(Matieres, Nummat=Nummat)

    if request.method == "POST":
        mat = request.POST["mat"]

        # Vérifier si les champs sont vides
        if mat:
            matiere.Mat = mat
            matiere.save()
            messages.success(request, "Modifié avec succès")
        else:
            messages.error(request, "Veuillez remplir tous les champs")

    return render(request, "updatemat.html", {"matieres": matiere})


# delete matiere


def deletem(request, nummat):
    prof = Matieres.objects.get(Nummat=nummat)
    prof.delete()
    return redirect("/filiere")



def emp(request):
    return render(request, 'affEmp.html')

def addc(request, filiere_id):
    profile = get_object_or_404(Profil, codeProfil=filiere_id)
    form = CoursForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            cours = form.save(commit=False)
            cours.NOPRFL_id = filiere_id  # Assign the filiere_id to the foreign key

            matricule = form.cleaned_data.get("Matricule")
            cd_horaire = form.cleaned_data.get("Cd_Horaire")
            num_jour = form.cleaned_data.get("NumJour")
            salle = form.cleaned_data.get("salle")

            existing_cours_prof = EmploisCours.objects.filter(
                Matricule=matricule, Cd_Horaire=cd_horaire, NumJour=num_jour
            ).exists()

            if existing_cours_prof:
                form.add_error(
                    None, "Ce professeur occupe déjà un cours à cette heure."
                )

            existing_cours_salle = EmploisCours.objects.filter(
                Cd_Horaire=cd_horaire, NumJour=num_jour, salle=salle
            ).exists()

            if existing_cours_salle:
                form.add_error(None, "Cette salle est déjà occupée à ce moment-là.")

            existing_cours_date = EmploisCours.objects.filter(
                Cd_Horaire=cd_horaire, NumJour=num_jour, NOPRFL_id=filiere_id
            ).exists()

            if existing_cours_date:
                form.add_error(
                    None, "Cette date et heure sont déjà occupées pour cette filière."
                )

            if existing_cours_prof or existing_cours_salle or existing_cours_date:
                context = {"form": form}
                return render(request, "addc.html", context=context, status=400)

            cours.save()
            return redirect("/filiere")

    else:
        form.fields["Mat"].queryset = Matieres.objects.filter(Noprfl_id=filiere_id)

    context = {
        "form": form,
    }

    # Mettre à jour les options de sélection des salles et des professeurs
    if request.method == "POST" and form.is_valid():
        cd_horaire = form.cleaned_data["Cd_Horaire"]
        num_jour = form.cleaned_data["NumJour"]

        salles_occupees = EmploisCours.objects.filter(
            Cd_Horaire=cd_horaire, NumJour=num_jour
        ).values_list('salle', flat=True)

        professeurs_occupees = EmploisCours.objects.filter(
            Cd_Horaire=cd_horaire, NumJour=num_jour
        ).values_list('Matricule', flat=True)

        form.fields["salle"].queryset = Salles.objects.exclude(id__in=salles_occupees)
        form.fields["Matricule"].queryset = Professeurs.objects.exclude(Matricule__in=professeurs_occupees)
        form.fields["salle"].queryset = Salles.objects.all()  # Liste complète des salles
        form.fields["Matricule"].queryset = Professeurs.objects.all()  # Liste complète des professeurs

    return render(request, "addc.html", context=context)
def occupancy_api(request):
    selected_horaire = request.GET.get('horaire')
    selected_jour = request.GET.get('jour')

    occupied_salles = EmploisCours.objects.filter(
        Cd_Horaire=selected_horaire,
        NumJour=selected_jour
    ).values_list('salle', flat=True)

    occupied_professeurs = EmploisCours.objects.filter(
        Cd_Horaire=selected_horaire,
        NumJour=selected_jour
    ).values_list('Matricule', flat=True)

    data = {
        'occupied_salles': list(occupied_salles),
        'occupied_professeurs': list(occupied_professeurs),
    }

    return JsonResponse(data)

def homeC(request, filiere_id):
    filiere = get_object_or_404(Profil, codeProfil=filiere_id)
    pr = EmploisCours.objects.filter(NOPRFL=filiere_id)
    context = {"Profil": filiere, "EmploisCours": pr}
    return render(request, "affichCours.html", context=context)


from django.http import JsonResponse

# def get_available_data(request):
#     cd_horaire = request.GET.get('cd_horaire')
#     num_jour = request.GET.get('num_jour')

#     salles_occupees = EmploisCours.objects.filter(
#         Cd_Horaire=cd_horaire, NumJour=num_jour
#     ).values_list('salle', flat=True)

#     professeurs_occupees = EmploisCours.objects.filter(
#         Cd_Horaire=cd_horaire, NumJour=num_jour
#     ).values_list('Matricule', flat=True)

#     salles_disponibles = Salles.objects.exclude(id__in=salles_occupees).values()
#     professeurs_disponibles = Professeurs.objects.exclude(Matricule__in=professeurs_occupees).values()

#     data = {
#         'salles': list(salles_disponibles),
#         'professeurs': list(professeurs_disponibles),
#     }

#     return JsonResponse(data)


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
    prof.delete()
    return redirect("/cours")




from django.shortcuts import render
from .models import EmploisCours


from datetime import date

def Emplois(request, code_profil):
    # Récupérer l'année en cours
    annee_en_cours = AnneeEnCours.objects.first()
    annee = annee_en_cours.annee if annee_en_cours else date.today().year

    # Calculer l'année précédente
    annee_precedente = annee - 1

    # Récupérer le profil correspondant
    profil = get_object_or_404(Profil, codeProfil=code_profil)
    jours = Jours.objects.all()
    heures = Horaire.objects.all()

    c_j_h = []
    cours = EmploisCours.objects.filter(NOPRFL=profil)
    for cours_item in cours:
        if cours_item.Cd_Horaire in heures and cours_item.NumJour in jours:
            c_j_h.append((cours_item.Mat, cours_item.NumJour, cours_item.Cd_Horaire, cours_item.Matricule, cours_item.salle))

    context = {
        'c_j_h': c_j_h,
        'jours': jours,
        'heures': heures,
        'profil': profil,
        'annee_en_cours': annee,
        'annee_precedente': annee_precedente
    }
    return render(request, 'Emplois.html', context)





from django.contrib.auth.models import User

def display_usernames(request):
    users = User.objects.all()  # Retrieve all user objects from the database
    return render(request, 'listrespo.html', {'users': users})



from io import BytesIO
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse
from io import BytesIO
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse
from bs4 import BeautifulSoup




def export_to_pdf(request, code_profil):
    profil = get_object_or_404(Profil, codeProfil=code_profil)
    annee_en_cours = AnneeEnCours.objects.first()
    annee = annee_en_cours.annee if annee_en_cours else date.today().year
    annee_precedente = annee - 1
    jours = Jours.objects.all()
    heures = Horaire.objects.all()

    c_j_h = []
    cours = EmploisCours.objects.filter(NOPRFL=profil)
    for cours_item in cours:
        if cours_item.Cd_Horaire in heures and cours_item.NumJour in jours:
            c_j_h.append(
                (
                    cours_item.Mat,
                    cours_item.NumJour,
                    cours_item.Cd_Horaire,
                    cours_item.Matricule,
                    cours_item.salle,
                )
            )

    # Rendu du template HTML avec les données
    context = {
        'annee_en_cours': annee,
        'annee_precedente': annee_precedente,
        "profil": profil,
        "jours": jours,
        "heures": heures,
        "c_j_h": c_j_h,
    }
    html = render_to_string("Emplois.html", context, request=request)
    html = '<meta charset="utf-8">' + '<link href="https://fonts.googleapis.com/css2?family=Amiri&display=swap" rel="stylesheet">' + html

    # Extract the desired <div> content
    soup = BeautifulSoup(html, "html.parser")
    div_content = soup.find("div", class_="row").prettify()
    style = """
   
 <style>

  .arabic {
    font-family: 'Amiri', Arial, sans-serif;
    
  }

  p {
    font-family: 'Amiri', Arial, sans-serif;
    text-align: center;
  }

  h1 {
    color: #333;
  }

table {
    border-collapse: collapse;
    width: 100%;
}

th, td {
    border: 1px solid #ccc;
    padding: 8px;
    
    text-align: center;
    
}
td{
    padding-right:15px;
    padding-buttom:10px;
    padding-top:10px;
}
 #p{
  position: absolute;
  top: 10px;
  left: 10px;
    }

    #p{
  position: absolute;
  top: 10px;
  right:10px;
    }

</style>
"""


    # Ajouter les liens vers les feuilles de style CSS avant le contenu de la <div>
    div_content = style + div_content

    # Nom du fichier PDF incluant le libellé de la filière
    filename = f"emplois_{profil.LibelleProfil}.pdf"

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    # Génération du PDF à partir du contenu HTML
    pdf = pisa.CreatePDF(div_content, dest=response, encoding="utf-8")

    if not pdf.err:
        return response

    return HttpResponse(f'Erreur lors de la génération du PDF pour le profil : {code_profil}')

    
def ListeEmplois(request):
    # Passer les données à la template
    filiere = Profil.objects.all()

    context = {
        "filieres": filiere,
    }

    # Rendre la template pour afficher les emplois de la filière
    return render(request, "ListeEmplois.html", context) 


from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from bs4 import BeautifulSoup
from xhtml2pdf import pisa
from .models import Jours, Horaire, EmploisCours

# Exportation de plusieurs Emplois

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import get_object_or_404

import pdfkit
from bs4 import BeautifulSoup
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import get_object_or_404

import pdfkit
from bs4 import BeautifulSoup
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from bs4 import BeautifulSoup
from xhtml2pdf import pisa
from .models import Profil, Jours, Horaire, EmploisCours

def export_to_pdfCollectif(request):
    code_filieres = request.POST.getlist('filieres')  # Récupérer la liste des codes de filières depuis la requête POST

    pdfs = []
    for code_filiere in code_filieres:
        profil = get_object_or_404(Profil, codeProfil=code_filiere)
        jours = Jours.objects.all()
        heures = Horaire.objects.all()

        c_j_h = []
        cours = EmploisCours.objects.filter(NOPRFL=profil)
        for cours_item in cours:
            if cours_item.Cd_Horaire in heures and cours_item.NumJour in jours:
                c_j_h.append(
                    (
                        cours_item.Mat,
                        cours_item.NumJour,
                        cours_item.Cd_Horaire,
                        cours_item.Matricule,
                        cours_item.salle,
                    )
                )

        # Rendu du template HTML avec les données
        context = {
            "profil": profil,
            "jours": jours,
            "heures": heures,
            "c_j_h": c_j_h,
        }
        html = render_to_string("Emplois.html", context, request=request)
        html = '<meta charset="utf-8">' + html
        # Extract the desired <div> content
        soup = BeautifulSoup(html, "html.parser")
        div_content = soup.find("div", class_="row").prettify()
        style = """
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Amiri&display=swap');

                .arabic {
                    font-family: 'Amiri', Arial, sans-serif;
                    direction: rtl;
                    text-align: right;
                }

                p {
                    font-family: Arial, sans-serif;
                    text-align: center;
                }

                h1 {
                    color: #333;
                }

                table {
                    border-collapse: collapse;
                    width: 100%;
                }

                th, td {
                    border: 1px solid #ccc;
                    padding: 8px;
                    text-align: center;
                }
                 #pf{
  position: absolute;
  top: 10px;
  left: 10px;
    }

    #pd{
  position: absolute;
  top: 10px;
  right:10px;
    }

            </style>
        """

        # Ajouter les liens vers les feuilles de style CSS avant le contenu de la <div>
        div_content = style + div_content

        # Génération du PDF à partir du contenu HTML
        pdf = pisa.CreatePDF(div_content, encoding="utf-8")

        if not pdf.err:
            pdfs.append((pdf, code_filiere))

    # Créer un fichier ZIP contenant tous les fichiers PDF générés
    zip_file = BytesIO()
    with zipfile.ZipFile(zip_file, "w") as zf:
        for pdf, code_filiere in pdfs:
            pdf_file_name = f"emplois_{code_filiere}.pdf"
            zf.writestr(pdf_file_name, pdf.dest.getvalue())

    # Retourner la réponse HTTP avec le fichier ZIP contenant les PDFs
    response = HttpResponse(content_type="application/zip")
    response["Content-Disposition"] = 'attachment; filename="emplois_collectifs.zip"'
    response.write(zip_file.getvalue())
    return response







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
