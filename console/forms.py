from django.forms import ModelForm
from django.core.exceptions import ValidationError
from core.models import App,Criterion


class AppForm(ModelForm):
	class Meta:
		model = App

class CriterionForm(ModelForm):
	class Meta:
		model = Criterion






