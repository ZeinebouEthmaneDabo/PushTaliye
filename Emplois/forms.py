from django import forms
from requests import request
from . models import DEPART, AnneeEnCours, EmploisCours, Grades, Horaire, Jours, Matieres, Profil, Professeurs, Salles
# rofil = forms.ModelChoiceField(queryset=Profil.objects.all())


class matForm(forms.ModelForm):
    class Meta:
        model = Matieres
        fields = ('Mat', 'Noprfl', 'Nummat')
    Mat = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    Noprfl = forms.ModelChoiceField(queryset=Profil.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}))
    Nummat = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control'}))
   

class ProfForm(forms.ModelForm):
    class Meta:
        model = Professeurs
        fields = "__all__"
    NNI = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    # Nodep = forms.ModelChoiceField(queryset=DEPART.objects.all(),
    #                                widget=forms.Select(attrs={'class': 'form-control'}))
    # Grade = forms.ModelChoiceField(queryset=Grades.objects.all(
    # ), widget=forms.Select(attrs={'class': 'form-control'}))
    Nom = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    Type = (
        ('Vacataire', 'Vacataire'),
        ('Permenant', 'Permenant'),

    )
    Type = forms.ChoiceField(choices=Type, widget=forms.Select(
        attrs={'class': 'form-control'}))
    Telephone = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control'}))
    Email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    CompteBancaire = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    Sexe = (
        ('Male', 'Male'),
        ('Femelle', 'Femelle'),

    )
    sexe = forms.ChoiceField(choices=Sexe, widget=forms.Select(
        attrs={'class': 'form-control'}))
   
    def __init__(self, *args, **kwargs):
        super(ProfForm, self).__init__(*args, **kwargs)

        self.fields["Grade"].label_from_instance = lambda obj: obj.nomGrade
        self.fields["Grade"].widget.attrs.update({"class": "form-control"})

        self.fields["Nodep"].label_from_instance = lambda obj: obj.Nom  
        self.fields["Nodep"].widget.attrs.update({"class": "form-control"})
 
    

  
     

class CoursForm(forms.ModelForm):
   
 
    class Meta:
        model = EmploisCours
        fields = [
            
            "Matricule",
            "Mat",
            "Cd_Horaire",
            "salle",
            "NumJour",
            "NatCours",
         
        ]
    
 
    def __init__(self, *args, **kwargs):
        super(CoursForm, self).__init__(*args, **kwargs)

        self.fields["Matricule"].label_from_instance = lambda obj: obj.Nom
        self.fields["Matricule"].widget.attrs.update({"class": "form-control"})

        self.fields["Mat"].label_from_instance = lambda obj: obj.Mat  
        self.fields["Mat"].widget.attrs.update({"class": "form-control"})
        
        
        self.fields["Cd_Horaire"].label_from_instance = lambda obj: obj.HCours  
        self.fields["Cd_Horaire"].widget.attrs.update({"class": "form-control"})

  
        self.fields["salle"] = forms.ModelChoiceField(
        queryset=Salles.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        )
        self.fields["salle"].label_from_instance = lambda obj: obj.NomSalles 
        self.fields["salle"].widget.attrs.update({"class": "form-control"})


        self.fields["NumJour"].label_from_instance = lambda obj: obj.NomJour 
        self.fields["NumJour"].widget.attrs.update({"class": "form-control"})

     

        self.fields["NatCours"].label_from_instance = lambda obj: obj.type 
        self.fields["NatCours"].widget.attrs.update({"class": "form-control"})
     