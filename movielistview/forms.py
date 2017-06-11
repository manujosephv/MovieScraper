from django import forms


# our new form
class ScrapeForm(forms.Form):
    scrape_pages = forms.IntegerField(required=True)
    min_rating = forms.FloatField(required=True)
    min_votes = forms.IntegerField(required=True)

class FilterForm(forms.Form):
    show_read = forms.BooleanField(required=False)
    min_rating = forms.FloatField(required=True)
    min_votes = forms.IntegerField(required=True)

class MarkReadForm(forms.Form):
    post_id = forms.IntegerField(required=True)
    checked = forms.CharField(max_length = 1,required=True)
  
class SearchMovieForm(forms.Form):
	condition_name = forms.CharField(max_length = 15, required = True)
	movie_name = forms.CharField(max_length = 200, required = False)
	condition_rating = forms.CharField(max_length = 15, required = True)
	rating = forms.FloatField(required=False)
	condition_votes = forms.CharField(max_length = 15, required = True)
	votes = forms.IntegerField(required = False)
	condition_date = forms.CharField(max_length = 15, required = True)
	date = forms.IntegerField(required = False)