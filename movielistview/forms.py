from django import forms

# our new form
class ScrapeForm(forms.Form):
    no_of_pages = forms.IntegerField(required=True)
    min_rating = forms.FloatField(required=True)
    min_votes = forms.IntegerField(required=True)