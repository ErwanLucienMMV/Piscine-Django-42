from django import forms


class MovieForm(forms.Form):
    title = forms.ChoiceField(label="Movie")

    def __init__(self, *args, titles, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].choices = [(title, title) for title in titles]
