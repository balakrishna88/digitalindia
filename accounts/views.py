import random
import string
from django.http import HttpResponse
from django.shortcuts import redirect, render
from accounts.forms import RegistrationForm
from .models import Account
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from accounts.forms import RegistrationForm
from .models import Account

#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import requests
from django.contrib import messages


def generate_random_suffix():
    """Generate a random string of digits."""
    return ''.join(random.choices(string.digits, k=4))

def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']

            # Check if the email already exists in the database
            if Account.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
                return redirect('register')

            # Check if the phone number already exists in the database
            if Account.objects.filter(phone_number=phone_number).exists():
                messages.error(request, 'Phone number already exists.')
                return redirect('register')

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            username_base = email.split("@")[0]
            username = username_base

            # Check if the username already exists in the database
            while Account.objects.filter(username=username).exists():
                # If the username exists, generate a random suffix and append it
                suffix = generate_random_suffix()
                username = f"{username_base}{suffix}"

            # Create the user with the unique username
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.is_active = True
            user.save()

            messages.success(request, 'You have successfully registered.')
            return redirect('register')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)
            

def login(request):
    if request.method =="POST":
        email= request.POST['email']
        password= request.POST['password']
        
        user= auth.authenticate(email=email,password=password)
        
        if user is not None:
            
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            url = request.META.get('HTTP_REFERER')
            try:
                query =requests.utils.urlparse(url).query
                
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('home')
        else:
            messages.error(request,"invalid login details")
            return redirect('login')
        
    return render(request, "accounts/login.html")


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,'logged out')
    return redirect('login')


def activate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError,OverflowError,Account.DoesNotExist):
        user =None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, 'congratulations! your accounts is activated')
        return redirect('login')
    else:
        messages.error(request,'invalid link')
        return redirect('register')
    

@login_required(login_url = 'login')   
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
    
    
def forgotpassword(request):
    if request.method=="POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            
             #user reset 
            current_site = get_current_site(request)
            mail_subject="reset your password"
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email=EmailMessage(mail_subject, message,to=[to_email])
            send_email.send()
            messages.success(request, 'password reset link sent to ur email')
            return redirect('login')
        
        else:
            messages.error(request, 'Account does not exists')
            return redirect('forgotpassword')
    
    return render(request, 'accounts/forgotpassword.html')


def resetpassword_validate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError,OverflowError,Account.DoesNotExist):
        user =None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request, 'reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request, 'This link is expired')
        return redirect('login')
        

def resetpassword(request):
    if request.method == 'POST':
        password= request.POST['password']
        confirm_password= request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)     
            user.save()
            messages.success(request,'password reset successful')
            return redirect('login')       
        else:
            messages.error(request, 'passwords does not match')
            return redirect('resetpassword')
    
    else:
      return render(request,'accounts/resetpassword.html')
    