from django import forms


class SearchForm(forms.Form):
    movies_minimum_release_date = forms.DateField(
        label="Movies minimum release date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    movies_maximum_release_date = forms.DateField(
        label="Movies maximum release date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    planet_diameter = forms.FloatField(label="Planet diameter greater than")
    character_gender = forms.ChoiceField(label="Character gender")

    def __init__(self, *args, genders, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["character_gender"].choices = [("", "Choose a gender")] + [
            (gender, gender) for gender in genders
        ]

    def clean(self):
        data = super().clean()
        minimum = data.get("movies_minimum_release_date")
        maximum = data.get("movies_maximum_release_date")
        if minimum and maximum and minimum > maximum:
            raise forms.ValidationError("The minimum release date must be on or before the maximum release date.")
        return data
