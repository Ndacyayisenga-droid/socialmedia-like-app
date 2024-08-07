from django.shortcuts import render, redirect, get_object_or_404
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
    if errors:
        for val in errors.values():
            messages.error(request, val)
        return redirect('/')
    
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
    if errors:
        for val in errors.values():
            messages.error(request, val)
        return redirect('/log')
    
    user = get_object_or_404(User, email=request.POST['email'])
    profile = get_object_or_404(Profile, user=user)
    request.session['user'] = profile.id
    return redirect('/xplanet/dashboard')

# Registered/New Profile Name Route
def success(request):
    if 'user' not in request.session:
        return redirect('/xplanet/no_user')
    
    user_profile = get_object_or_404(Profile, id=request.session['user'])
    context = {
        'User': user_profile,
        'status': request.session['word']
    }
    return render(request, 'success.html', context)

def ProName(request):
    errors = Profile.objects.valid_Name(request.POST)
    if errors:
        for val in errors.values():
            messages.error(request, val)
        return redirect('/success')
    
    profile = get_object_or_404(Profile, id=request.session['user'])
    profile.name = request.POST['proname']
    profile.save()
    return redirect('/xplanet/dashboard')

# Logout Route
def logout(request):
    request.session.clear()
    return redirect('/')
