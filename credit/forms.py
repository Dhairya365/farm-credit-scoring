from django import forms

class SoilHealthForm(forms.Form):
    nitrogen = forms.FloatField()
    phosphorus = forms.FloatField()
    potassium = forms.FloatField()
    ph = forms.FloatField()
    organic_carbon = forms.FloatField()
    city = forms.CharField()
    farm_size = forms.FloatField()
