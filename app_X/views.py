from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Post, Comment

# Helper Functions
def get_user_profile(request):
    """Helper function to get the user profile from the session."""
    return get_object_or_404(Profile, id=request.session['user'])

def get_common_context(request):
    """Helper function to get common context data for views."""
    user_profile = get_user_profile(request)
    return {
        'User': user_profile,
        'Following': user_profile.following.all(),
        'Followers': user_profile.followers.all(),
        'status': request.session.get('word', '')
    }

def redirect_if_no_user(request):
    """Helper function to redirect if no user is logged in."""
    if 'user' not in request.session:
        return redirect('no_user')
    return None

# WISE WELCOME_________
def xplanet(request):
    context = {}
    if 'user' in request.session:
        context['User'] = get_user_profile(request)
        context['status'] = request.session.get('word', '')
    else:
        context['No_user'] = "Not Signed In!"
    return render(request, 'wisewelcome.html', context)

def no_user(request):
    return render(request, 'nouser.html')

# DASHBOARD PAGE FUNCTIONS________
def dashboard(request):
    if redirect_if_no_user(request):
        return redirect('no_user')

    user_profile = get_user_profile(request)
    context = get_common_context(request)
    context.update({
        'User_liked': user_profile.posts_liked.all().order_by("-id"),
        'User_comments': user_profile.profile_comments.all().order_by("-id"),
        'Posts': user_profile.posts.all().order_by("-id"),
    })
    return render(request, 'dashboard.html', context)

# FORUM PAGE FUNCTIONS _________
def forum(request):
    if redirect_if_no_user(request):
        return redirect('no_user')

    context = get_common_context(request)
    context['Posts'] = Post.objects.all().order_by('-id')
    return render(request, 'forum.html', context)

def post(request):
    request.session['word'] = 'post'
    errors = Post.objects.valid_post(request.POST)
    if errors:
        for val in errors.values():
            messages.error(request, val)
        return redirect('forum')

    Post.objects.create(
        title=request.POST['title'],
        post=request.POST['post'],
        profile=get_user_profile(request)
    )
    return redirect('forum')

def viewpost(request, num):
    if redirect_if_no_user(request):
        return redirect('no_user')

    context = get_common_context(request)
    context['Post'] = get_object_or_404(Post, id=num)
    return render(request, 'postview.html', context)

def editpost(request):
    request.session['word'] = 'post'
    errors = Post.objects.valid_post(request.POST)
    if errors:
        for val in errors.values():
            messages.error(request, val)
        return redirect(f'viewpost/{request.POST["ekey"]}')

    post = get_object_or_404(Post, id=request.POST['ekey'])
    post.post = request.POST['post']
    post.title = request.POST['title']
    post.save()
    return redirect(f'viewpost/{request.POST["ekey"]}')

def comment(request):
    request.session['word'] = 'comment'
    errors = Comment.objects.valid_comment(request.POST)
    if errors:
        for val in errors.values():
            messages.error(request, val)
        return redirect('forum')

    Comment.objects.create(
        post=get_object_or_404(Post, id=request.POST['comkey']),
        profile=get_user_profile(request),
        comment=request.POST['comment']
    )
    return redirect('forum')

def delete(request):
    post = get_object_or_404(Post, id=request.POST['delkey'])
    post.delete()
    return redirect('forum')

# LIKES/DISLIKES_____________________
def like(request):
    user = get_user_profile(request)
    post = get_object_or_404(Post, id=request.POST['jugkey'])
    post.liked.add(user)
    return redirect('forum')

def dislike(request):
    user = get_user_profile(request)
    post = get_object_or_404(Post, id=request.POST['jugkey'])
    post.liked.remove(user)
    return redirect('forum')

# Settings Page________________
def settings(request):
    if redirect_if_no_user(request):
        return redirect('no_user')

    context = get_common_context(request)
    return render(request, 'settings.html', context)

def update(request):
    profile = get_user_profile(request)
    errors = Profile.objects.valid_pro(request.POST, request.session)
    if errors:
        for val in errors.values():
            messages.error(request, val)
        return redirect('settings')

    if 'name' in request.POST:
        profile.name = request.POST['name']
    if 'bio' in request.POST:
        profile.bio = request.POST['bio']
    if 'image' in request.FILES:
        profile.image = request.FILES['image']
    profile.save()
    return redirect('settings')

# Humans Page
def humans(request):
    if redirect_if_no_user(request):
        return redirect('no_user')

    context = get_common_context(request)
    context['All'] = Profile.objects.all().order_by('name')
    return render(request, 'humans.html', context)

def follow(request, num):
    me = get_user_profile(request)
    you = get_object_or_404(Profile, id=num)
    you.followers.add(me)
    me.following.add(you)
    return redirect('humans')

def unfollow(request, num):
    me = get_user_profile(request)
    you = get_object_or_404(Profile, id=num)
    you.followers.remove(me)
    me.following.remove(you)
    return redirect('humans')

# View Human
def viewhuman(request, name):
    context = get_common_context(request)
    them_profile = get_object_or_404(Profile, name=name)
    context.update({
        'Them': them_profile,
        'Them_liked': them_profile.posts_liked.all().order_by("-id"),
        'Them_comments': them_profile.profile_comments.all().order_by("-id"),
        'Posts': them_profile.posts.all().order_by("-id"),
    })
    return render(request, 'viewhuman.html', context)

# News Feed Page_____________
def news(request):
    if redirect_if_no_user(request):
        return redirect('no_user')

    context = get_common_context(request)
    context['Posts'] = Post.objects.all().order_by('-id')
    return render(request, 'newsfeed.html', context)
