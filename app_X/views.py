from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages


# Create your views here.

# WISE WELCOME_________
def xplanet(request):
    if 'user' in request.session:
        context = {
            'User': Profile.objects.get(id=request.session['user']),
            'status': request.session['word'],
        }
    else:
        context = {
            'No_user': "Not Signed In!"
        }
    return render(request, 'wisewelcome.html', context)

def no_user(request):
    return render(request, 'nouser.html')


# DASHBOARD PAGE FUNCTIONS________
def dashboard(request):
    if 'user' not in request.session:
        return redirect('/xplanet/no_user')
    context = {
        'User': Profile.objects.get(id=request.session['user']),
        'User_liked': Profile.objects.get(id=request.session['user']).posts_liked.all().order_by("-id"),
        'User_comments': Profile.objects.get(id=request.session['user']).profile_comments.all().order_by("-id"),
        'Posts': Profile.objects.get(id=request.session['user']).posts.all().order_by("-id"),
        'Following': Profile.objects.get(id=request.session['user']).following.all(),
        'Followers': Profile.objects.get(id=request.session['user']).followers.all(),
        'status': request.session['word']
    }
    return render(request, 'dashboard.html', context)


# FORUM PAGE FUNCTIONS _________
def forum(request):
    if 'user' not in request.session:
        return redirect('/xplanet/no_user')
    context = {
        'User': Profile.objects.get(id=request.session['user']),
        'status': request.session['word'],
        'Posts': Post.objects.all().order_by('-id'),
        'Following': Profile.objects.get(id=request.session['user']).following.all(),
        'Followers': Profile.objects.get(id=request.session['user']).followers.all(),
    }
    return render(request, 'forum.html', context)

def post(request):
    request.session['word'] = 'post'
    errors = Post.objects.valid_post(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            print(key)
            messages.error(request, val)
        return redirect('/xplanet/forum')
    else:
        Post.objects.create(
            title=request.POST['title'],
            post=request.POST['post'],
            profile=Profile.objects.get(id=request.session['user'])
        )
    return redirect('/xplanet/forum')

def viewpost(request, num):
    if 'user' not in request.session:
        return redirect('/xplanet/no_user')
    context = {
        'User': Profile.objects.get(id=request.session['user']),
        'status': request.session['word'],
        'Post': Post.objects.get(id=num),
        'Following': Profile.objects.get(id=request.session['user']).following.all(),
        'Followers': Profile.objects.get(id=request.session['user']).followers.all(),
    }
    return render(request, 'postview.html', context)

def editpost(request):
    request.session['word'] = 'post'
    errors = Post.objects.valid_post(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/xplanet/viewpost/'+request.POST['ekey'])
    else:
        post = Post.objects.get(id=request.POST['ekey'])
        post.post=request.POST['post']
        post.title=request.POST['title']
        post.save()
    return redirect('/xplanet/viewpost/'+request.POST['ekey'])

def comment(request):
    request.session['word'] = 'comment'
    errors = Comment.objects.valid_comment(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/xplanet/forum')
    else:
        Comment.objects.create(
            post=Post.objects.get(id=request.POST['comkey']),
            profile=Profile.objects.get(id=request.session['user']),
            comment=request.POST['comment']
        )
    return redirect('/xplanet/forum')

def delete(request):
    c = Post.objects.get(id=request.POST['delkey'])
    c.delete()
    return redirect('/xplanet/forum')

    # LIKES/DISLIKES_____________________
def like(request):
    user = Profile.objects.get(id=request.session['user'])
    post = Post.objects.get(id=request.POST['jugkey'])
    post.liked.add(user)
    return redirect('/xplanet/forum')

def dislike(request):
    user = Profile.objects.get(id=request.session['user'])
    post = Post.objects.get(id=request.POST['jugkey'])
    post.liked.remove(user)
    return redirect('/xplanet/forum')

# Settings Page________________
def settings(request):
    if 'user' not in request.session:
        return redirect('/xplanet/no_user')
    context = {
        'User': Profile.objects.get(id=request.session['user']),
        'Following': Profile.objects.get(id=request.session['user']).following.all(),
        'Followers': Profile.objects.get(id=request.session['user']).followers.all(),
        'status': request.session['word']
    }
    return render(request, 'settings.html', context)

def update(request):
    print('Step: 1')
    profile = Profile.objects.get(id=request.session['user'])
    errors = Profile.objects.valid_pro(request.POST, request.session)
    if len(errors) > 0:
        print('Step: 2')
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/xplanet/settings')
    else:
        print('Step: 3')
        if 'name' in request.POST:
            profile.name=request.POST['name']
            profile.save()
        if 'bio' in request.POST:
            profile.bio=request.POST['bio']
            profile.save()
        if 'image' in request.FILES:
            profile.image=request.FILES['image']
            print(profile.image.name)
            print(profile.image.size)
            profile.save()
    return redirect('/xplanet/settings')

# Humans Page
def humans(request):
    if 'user' not in request.session:
        return redirect('/xplanet/no_user')
    context = {
        'User': Profile.objects.get(id=request.session['user']),
        'Following': Profile.objects.get(id=request.session['user']).following.all(),
        'Followers': Profile.objects.get(id=request.session['user']).followers.all(),
        'status': request.session['word'],
        'All': Profile.objects.all().order_by('name')
    }
    return render(request, 'humans.html', context)

def follow(request, num):
    me = Profile.objects.get(id=request.session['user'])
    you = Profile.objects.get(id=num)
    you.followers.add(me)
    me.following.add(you)
    return redirect('/xplanet/humans')

def unfollow(request, num):
    me = Profile.objects.get(id=request.session['user'])
    you = Profile.objects.get(id=num)
    you.followers.remove(me)
    me.following.remove(you)
    return redirect('/xplanet/humans')

# View Human
def viewhuman(request, name):
    context = {
        'User': Profile.objects.get(id=request.session['user']),
        'Them': Profile.objects.get(name=name),
        'Them_liked': Profile.objects.get(name=name).posts_liked.all().order_by("-id"),
        'Them_comments': Profile.objects.get(name=name).profile_comments.all().order_by("-id"),
        'Posts': Profile.objects.get(name=name).posts.all().order_by("-id"),
        'Following': Profile.objects.get(name=name).following.all(),
        'Followers': Profile.objects.get(name=name).followers.all(),
        'status': request.session['word']
    }
    return render(request, 'viewhuman.html', context)

# News Feed Page_____________
def news(request):
    if 'user' not in request.session:
        return redirect('/xplanet/no_user')
    context = {
        'User': Profile.objects.get(id=request.session['user']),
        'status': request.session['word'],
        'Posts': Post.objects.all().order_by('-id'),
        'Following': Profile.objects.get(id=request.session['user']).following.all(),
        'Followers': Profile.objects.get(id=request.session['user']).followers.all(),
    }
    return render(request, 'newsfeed.html', context)