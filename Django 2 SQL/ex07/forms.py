from django import forms


class MovieForm(forms.Form):
    title = forms.ChoiceField(label="Movie")

    opening_crawl = forms.CharField(label="Opening crawl", widget=forms.Textarea, required=False, strip=False)

    def __init__(self, *args, titles, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].choices = [(title, title) for title in titles]
