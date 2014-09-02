from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def unique_username(value):
	if User.objects.filter(username = value).exists():
		raise ValidationError(u'%s already exists' % value)

class UserForm(forms.Form):
	username = forms.CharField(label = "User name", validators = [unique_username])
	password = forms.CharField()
	confirm_password = forms.CharField(widget = forms.PasswordInput)
	name = forms.CharField(label = "First name")
	last_name = forms.CharField()
	email = forms.EmailField(label = "Email adress")

	def clean(self):
		cleaned_data = super(UserForm,self).clean()
		pass1 = cleaned_data.get("password")
		pass2 = cleaned_data.get("confirm_password")
		if pass1 != pass2 :
			raise forms.ValidationError("Passwords does not match")
		return cleaned_data





