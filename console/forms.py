from django.forms import ModelForm
from django.core.exceptions import ValidationError
from core.models import App


class AppForm(ModelForm):
	class Meta:
		model = App






