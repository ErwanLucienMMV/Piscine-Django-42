from django import forms


class EntryForm(forms.Form):
    text = forms.CharField(label="Texte", strip=True)
