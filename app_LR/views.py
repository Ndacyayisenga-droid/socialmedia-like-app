from django.shortcuts import render, redirect, HttpResponse
from .models import User
from app_X.models import Profile
from django.contrib import messages
import bcrypt

# Create your views here.

def indexReg(request):
    return render(request, 'indexReg.html')

def indexLog(request):
    return render(request, 'indexLog.html')

# Register Route
def register(request):
    request.session.clear()
    request.session['reg'] = 1
    request.session['word'] = 'Registered'
    errors = User.objects.user_validation(request.POST)
    if len(errors) > 0:
        print(len(errors),'ERRORS!')
        for key, val in errors.items():
            print(key,val)
            messages.error(request, val)
        return redirect('/')
    else:
        print('No errors')
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name=request.POST['fname'],
            last_name=request.POST['lname'],
            email=request.POST['email'],
            password=pw_hash
        )
        profile = Profile.objects.create(user=user)
        request.session['user'] = profile.id
    return redirect('/success')

# Login Route
def login(request):
    request.session.clear()
    request.session['log'] = 1
    request.session['word'] = 'Logged In'
    errors = User.objects.login_validation(request.POST)
    if len(errors) > 0:
        print(len(errors),'ERRORS!')
        for key, val in errors.items():
            print(key,val)
            messages.error(request, val)
        return redirect('/log')
    else:
        print('No errors')
        user = User.objects.get(email=request.POST['email'])
        profile = Profile.objects.get(user=user)
        request.session['user'] = profile.id
    return redirect('/xplanet/dashboard')

# Registered/New Profile Name Route
def success(request):
    if 'user' not in request.session:
        return redirect('/xplanet/no_user')
    context = {
        'User': Profile.objects.get(id=request.session['user']),
        'status': request.session['word']
    }
    return render(request, 'success.html', context)

def ProName(request):
    errors = Profile.objects.valid_Name(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/success')
    else:
        profile = Profile.objects.get(id=request.session['user'])
        profile.name=request.POST['proname']
        profile.save()
    return redirect('/xplanet/dashboard')

# Logout Route
def logout(request):
    request.session.clear()
    return redirect('/')