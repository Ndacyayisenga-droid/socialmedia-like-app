from django.urls import path
from . import views

urlpatterns = [
    # Wise Welcome
    path('', views.xplanet),
    
    # Redirect for Non-Users
    path('no_user', views.no_user),

    # User Dashboard
    path('dashboard', views.dashboard),

    # Forum Routes
    path('forum', views.forum),
    path('post', views.post),
    path('viewpost/<int:num>', views.viewpost),
    path('editpost', views.editpost),
    path('comment', views.comment),
    path('delete', views.delete),

    # LIKES/DISLIKES
    path('like', views.like),
    path('dislike', views.dislike),

    # Settings
    path('settings', views.settings),
    path('update', views.update),

    # Humans
    path('humans', views.humans),
    path('follow/<int:num>', views.follow),
    path('unfollow/<int:num>', views.unfollow),
    path('viewhuman/<name>', views.viewhuman),

    # News Feed
    path('news', views.news),
]