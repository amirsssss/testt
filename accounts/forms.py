from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
# from django.core.validators import RegexValidator



User=get_user_model()

class UserLoginForm(forms.Form):
	phone_num= forms.CharField(label="Phone Number")
	password = forms.CharField(label='Password', widget=forms.PasswordInput)


	def clean(self,*args,**kwargs):
		phone_num=self.cleaned_data.get("phone_num")
		password=self.cleaned_data.get("password")

		phone_num_obj=User.objects.filter(phone_num=phone_num).first()
		if not phone_num_obj:
			raise forms.ValidationError("شما هنوز ثبت نام نکرده اید از طریق تلفن همراه ثبت نام نمایید .")
		else:
		   if not phone_num_obj.check_password(password):
			   raise forms.ValidationError("Invalid Credential")
		return super(UserLoginForm,self).clean(*args,**kwargs)

	# def __init__(self, *args, **kwargs):
	# 	self.helper = FormHelper()
	# 	self.helper.layout = Layout(
	# 		Fieldset(
	# 			'',
	# 			'phone_num',
	# 			'password'
	# 		),
	# 		ButtonHolder(
	# 			Submit('submit', 'Login', css_class='btn btn-primary btn-lg')
	# 		)
	# 	)
	# 	super(UserLoginForm, self).__init__(*args, **kwargs)


	#Login with Password
	# phone_num= forms.CharField(label="Phone Number")
	# password = forms.CharField(label='Password', widget=forms.PasswordInput)

	# def clean(self,*args,**kwargs):
	#	 phone_num=self.cleaned_data.get("phone_num")
	#	 password=self.cleaned_data.get("password")

	#	 phone_num_obj=User.objects.filter(phone_num=phone_num).first()
	#	 if not phone_num_obj:
	#		 raise forms.ValidationError("Invalid Credential")
	#	 else:
	#		 if not phone_num_obj.check_password(password):
	#			 raise forms.ValidationError("Invalid Credential")
	#	 return super(UserLoginForm,self).clean(*args,**kwargs)

	# def __init__(self, *args, **kwargs):
	#	 self.helper = FormHelper()
	#	 self.helper.layout = Layout(
	#		 Fieldset(
	#			 '',
	#			 'phone_num',
	#			 'password'
	#		 ),
	#		 ButtonHolder(
	#			 Submit('submit', 'Login', css_class='btn btn-primary btn-lg')
	#		 )
	#	 )
	#	 super(UserLoginForm, self).__init__(*args, **kwargs)


class UserCreationForm(forms.ModelForm):
	"""A form for creating new users. Includes all the required
	fields, plus a repeated password."""
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
	# activationcode = forms.CharField(label='activationcode', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('phone_num',)

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			#idea:
			# if.user.is_active:
			# 	user.save()
			user.save()
		return user

	# def __init__(self, *args, **kwargs):
	# 	self.helper = FormHelper()
	# 	self.helper.layout = Layout(
	# 		Fieldset(
	# 			'',
	# 			'phone_num',
	# 			'password1',
	# 			'password2'
	# 		),
	# 		ButtonHolder(
	# 			Submit('submit', 'Register', css_class='btn btn-primary btn-lg')
	# 		)
	# 	)
	# 	super(UserCreationForm, self).__init__(*args, **kwargs)

	#registration with password
	# password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	# password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	# class Meta:
	#	 model = User
	#	 fields = ('phone_num',)

	# def clean_password2(self):
	#	 # Check that the two password entries match
	#	 password1 = self.cleaned_data.get("password1")
	#	 password2 = self.cleaned_data.get("password2")
	#	 if password1 and password2 and password1 != password2:
	#		 raise forms.ValidationError("Passwords don't match")
	#	 return password2

	# def save(self, commit=True):
	#	 # Save the provided password in hashed format
	#	 user = super().save(commit=False)
	#	 user.set_password(self.cleaned_data["password1"])
	#	 if commit:
	#		 user.save()
	#	 return user

	# def __init__(self, *args, **kwargs):
	#	 self.helper = FormHelper()
	#	 self.helper.layout = Layout(
	#		 Fieldset(
	#			 '',
	#			 'phone_num',
	#			 'password1',
	#			 'password2'
	#		 ),
	#		 ButtonHolder(
	#			 Submit('submit', 'Register', css_class='btn btn-primary btn-lg')
	#		 )
	#	 )
	#	 super(UserCreationForm, self).__init__(*args, **kwargs)


class UserChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ('phone_num', 'password', 'is_staff','is_active', 'is_admin')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]

class UserActivation(forms.Form):
	activationkey=forms.CharField(max_length=10,label="Enter the code sent to You by SMS",widget=forms.TextInput(attrs={'placeholder': 'Activation Code'}))

	# def clean_key(self,*args,**kwargs):
	# 	activationkey=self.cleaned_data.get('activationkey')
	# 	print('activationkey in form'+activationkey)
	# 	return super(UserActivation,self).clean(*args,**kwargs)

	# def __init__(self, *args, **kwargs):
	# 	self.helper = FormHelper()
	# 	self.helper.layout = Layout(
	# 		Fieldset(
	# 			'',
	# 			'activationkey'
	# 		),
	# 		ButtonHolder(
	# 			Submit('submit', 'Active', css_class='btn btn-primary btn-lg')
	# 		)
	# 	)
	# 	super(UserActivation, self).__init__(*args, **kwargs)



# class SetPasswordForm(forms.Form):
# 	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
# 	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

# 	def clean_password2(self):
# 		# Check that the two password entries match
# 		password1 = self.cleaned_data.get("password1")
# 		password2 = self.cleaned_data.get("password2")

# 		if password1 and password2 and password1 != password2:
# 			raise forms.ValidationError("Passwords don't match")
# 		return password2

# 	def __init__(self, *args, **kwargs):
# 		self.helper = FormHelper()
# 		self.helper.layout = Layout(
# 			Fieldset(
# 				'',
# 				'password1',
# 				'password2'
# 			),
# 			ButtonHolder(
# 				Submit('submit', 'Confirm', css_class='btn btn-primary btn-lg')
# 			)
# 		)
# 		super(SetPasswordForm, self).__init__(*args, **kwargs)