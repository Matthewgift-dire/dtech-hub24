from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as error_message
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

def convert_username(username):
		username.lower()
		
class SignupForm(UserCreationForm):
	
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']
		
	username = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'email_text',
				'placeholder': 'username'
			}
		),
		label='',
		required=True,
		validators=[convert_username, User.username_validator]
	)
	
	password1 = forms.CharField(
		widget=forms.PasswordInput(
			attrs={
				'class': 'email_text',
				'placeholder': 'password'
			}
		),
		label='',
	)


	password2 = forms.CharField(
		widget=forms.PasswordInput(
			attrs={
				'class': 'email_text',
				'placeholder': 'comfirm password'
			}
		),
		label='',
	)
	

class LoginForm(forms.Form):
    username = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'email_text',
				'placeholder': 'username'
			}
		),
		label='',
		required=True
	)
	
    password = forms.CharField(
		widget=forms.PasswordInput(
			attrs={
				'class': 'email_text',
				'placeholder': 'password'
			}
		),
		label='',
		required=True
	)


def validate_comment(comment):
	if not comment.isnumeric():
		cleaned_comment = comment.lower().split()
		with open('links.txt', 'r') as links:
			links = links.readlines()
			for link in links:
				if link.strip('\n') in cleaned_comment:
					raise ValidationError(
						error_message("affiliate links not allowed!")
					)
						
		with open("badwords.txt", 'r') as bad_words:
			bad_words = bad_words.readlines()
			for word in bad_words:
				if word.strip('\n') in cleaned_comment:
					raise ValidationError(
						error_message("This blog don't condole abusive words!")
					)
					
	else:
		raise ValidationError(
			error_message("comments must contain alphabets")
		)
		
						
class CommentForm(forms.Form):
	body = forms.CharField(
		max_length=255,
		min_length=3,
		widget=forms.Textarea(
			attrs={
				"class": 'form-control',
				"placeholder": 'Say something...',
				"style": 'color:black;',
				"style": 'background-color:aliceblue;'
			}
		),
		required=True,
		label='',
		validators=[validate_comment]
	)
	

class ContactForm(forms.Form):
	name = forms.CharField(
		min_length=4,
		widget=forms.TextInput(
			attrs={
				'class': 'email_text',
				'placeholder': 'Name'
			}
		),
		label='',
		required=True
	)
	
	email = forms.CharField(
		max_length=30,
		widget=forms.EmailInput(
			attrs={
				'class': 'email_text',
				'placeholder': 'Email'
			}
		),
		label='',
		required=True,
		validators=[EmailValidator()]
	)
	
	subject = forms.CharField(
		max_length=35,
		widget=forms.TextInput(
			attrs={
				'class': 'email_text',
				'placeholder': 'Subject'
			}
		),
		label='',
		required=True
	)
	
	message = forms.CharField(
		min_length=20,
		widget=forms.Textarea(
			attrs={
				'class': 'email_text',
				'placeholder': 'Message',
				'id': 'comment',
				'rows': 5,
			}
		),
		label='',
		required=True
	)