from django.contrib.auth import login,logout,get_user_model
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
import requests
from .forms import UserCreationForm,UserChangeForm,UserLoginForm,UserActivation
from .models import ActivationCode,ActivationUrl,SetPasswordUrl


url = "https://api.kavenegar.com/v1/6D3477306C61385547574A78716F516C37664E6972413D3D/sms/send.json"

User=get_user_model()


def home(request):
	if request.user.is_authenticated and request.user.is_active:
		return render(request,"accounts/dashboard.html",{})
	return HttpResponseRedirect("/login/")


def register(request,*args,**kwargs):
	form=UserCreationForm(request.POST or None)
	if form.is_valid():
		form.save()
		phone_number_=form.cleaned_data.get("phone_num")
		user_obj=User.objects.get(phone_num__iexact=phone_number_)
		key_sms=ActivationCode.objects.all().get(user=user_obj).key

		reciever = str(phone_number_)
		PM = "کد فعال سازی شما در سایت بسته ی من "+str(key_sms)
		parameters = {'receptor': reciever, 'message': PM}

		r = requests.get(url, params=parameters)

		urlcode=ActivationUrl.objects.filter(user=user_obj).first().urlkey
		return HttpResponseRedirect("/activation/"+urlcode)
	return render(request,"accounts/register.html",{"form":form})


def logout_view(request):
	logout(request)
	return HttpResponseRedirect("/")

def urlactivation_view(request,urlcode=None,*args,**kwargs):
	form=UserActivation(request.POST or None)
	user_object=ActivationUrl.objects.get(urlkey=urlcode).user
	if form.is_valid():
		ecode_qs=form.cleaned_data.get("activationkey")
		acc_profile_qs=ActivationCode.objects.all().filter(key=ecode_qs).first()
		true_acc=ActivationCode.objects.get(user=user_object)
		if not acc_profile_qs==None and true_acc==acc_profile_qs:
			if not acc_profile_qs.expired:
				user_obj=acc_profile_qs.user
				user_obj.is_active=True
				user_obj.save()
				acc_profile_qs.expired=True
				acc_profile_qs.save()
				return render(request,'accounts/activated.html',{"form":form})
		else:
			return render(request,'accounts/activation.html',{"form":form,"message":"Wrong Activation Code"})
	return render(request,'accounts/activation.html',{"form":form})

def login_view(request,*args,**kwargs):
	if request.user.is_authenticated:
		return render(request,"accounts/dashboard.html",{})
	else:
		form=UserLoginForm(request.POST or None)
		if form.is_valid():
			phonenumber_=form.cleaned_data.get("phone_num")
			user_obj=User.objects.get(phone_num__iexact=phonenumber_)
			if user_obj.is_active:
				login(request,user_obj)
				return render(request,"accounts/dashboard.html",{})
			else:
				return HttpResponse("Your account is not activated!")
		return render(request,"accounts/login.html",{"form":form})


#assing pass after entering phone number
# def login_view(request,*args,**kwargs):
# 	form=UserLoginForm(request.POST or None)
# 	if form.is_valid():
# 		phonenumber_=form.cleaned_data.get("phone_num")
# 		user_obj=User.objects.get(phone_num__iexact=phonenumber_)
# 		login(request,user_obj)
# 		passurl=SetPasswordUrl.objects.filter(user=user_obj).first().passurlkey
# 		print('-'*40)
# 		print(passurl)
# 		return HttpResponseRedirect("/setpassword/"+passurl)
# 	return render(request,"accounts/login.html",{"form":form})


# def setpass_view(request,passurl=None,*args,**kwargs):
# 	form=SetPasswordForm(request.POST or None)
# 	user_object=SetPasswordUrl.objects.get(passurlkey=passurl).user
# 	print(user_object)
# 	print(type(user_object))
# 	# org_user=User.objects.get(phone_num__iexact=user_object)
# 	print(form.is_valid())
# 	if form.is_valid():
# 		print('*-'*10)
# 		pass_qs=form.cleaned_data.get("password1")
# 		print(pass_qs)
# 		user_object.set_password(pass_qs)
# 		user_object.save()
# 		return render(request,'accounts/passwordset.html')

# 	return render(request,'accounts/setpass.html',{"form":form})
