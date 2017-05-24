from django import forms


# our new form
class ScrapeForm(forms.Form):
    scrape_pages = forms.IntegerField(required=True)
    min_rating = forms.FloatField(required=True)
    min_votes = forms.IntegerField(required=True)

class FilterForm(forms.Form):
    show_read = forms.CharField(max_length = 1,required=True)
    min_rating = forms.FloatField(required=True)
    min_votes = forms.IntegerField(required=True)

class MarkReadForm(forms.Form):
    post_id = forms.IntegerField(required=True)
    