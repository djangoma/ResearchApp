from django import forms
from .models import JournalArticle, ConferenceArticle, Project, BookSeries
from django.forms import ModelForm
from .models import Document

class DocumentForm(forms.ModelForm):
	class Meta:
		model = Document
		fields = ('description', 'document',)

class JournalNewForm(forms.ModelForm):
    '''message = forms.CharField(widget=forms.Textarea(), max_length=100)'''

    class Meta:
        model = JournalArticle
        fields = '__all__'
	
class JournalUpdateForm(forms.ModelForm):
	class Meta:
		model = JournalArticle
		fields = '__all__'

class ConferenceNewForm(forms.ModelForm):
    '''message = forms.CharField(widget=forms.Textarea(), max_length=100)'''

    class Meta:
        model = ConferenceArticle
        fields = '__all__'
	
class ConferenceUpdateForm(forms.ModelForm):
	class Meta:
		model = ConferenceArticle
		fields = '__all__'
		
class ProjectNewForm(forms.ModelForm):
    '''message = forms.CharField(widget=forms.Textarea(), max_length=100)'''

    class Meta:
        model = Project
        fields = '__all__'
	
class ProjectUpdateForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = '__all__'
		
class BookSeriesNewForm(forms.ModelForm):
    '''message = forms.CharField(widget=forms.Textarea(), max_length=100)'''

    class Meta:
        model = BookSeries
        fields = '__all__'
	
class BookSeriesUpdateForm(forms.ModelForm):
	class Meta:
		model = BookSeries
		fields = '__all__'