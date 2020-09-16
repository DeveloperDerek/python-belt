from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('adding_user', views.adding_user),
    path('wishes', views.wishes),
    path('wishes/new', views.new_wish),
    path('login', views.login),
    path('logout', views.logout),
    path('making_wish', views.making_wish),
    path('grant_wish/<int:id>', views.grant_wish),
    path('liking_wish/<int:id>', views.liking_wish),
    path('unliking_wish/<int:id>', views.unliking_wish),
    path('remove/<int:id>', views.remove),
    path('edit/<int:id>', views.edit),
    path('edit_wish/<int:id>', views.edit_wish),
    path('stats', views.stats)
]