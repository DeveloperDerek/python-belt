from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def logout(request):
    request.session.clear()
    return redirect('/')

def wishes(request):
    context = {
        'user' : User.objects.get(id=request.session['current_user']),
        'wishes' : Wish.objects.all()
    }
    return render(request, 'wishes.html', context)

def new_wish(request):
    context = {
        'user' : User.objects.get(id=request.session['current_user'])
    }
    return render(request, 'new_wish.html', context)

def edit(request, id):
    context = {
        'user' : User.objects.get(id=request.session['current_user']),
        'wish' : Wish.objects.get(id=id)
    }
    return render(request, 'edit.html', context)


def stats(request):
    me = User.objects.get(id=request.session['current_user'])
    wishes = Wish.objects.filter(grant = True)
    my_wish = Wish.objects.filter(wished_by = me).filter(grant = True).count()
    not_yet = Wish.objects.filter(wished_by = me).filter(grant = False).count()
    context = {
        'wishes' : wishes,
        'user' : me,
        'pos' : my_wish,
        'neg' : not_yet
    }
    return render(request, 'stats.html', context)


def making_wish(request):
    errors = Wish.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wishes/new')
    me = User.objects.get(id=request.session['current_user'])
    new_wish = Wish.objects.create(
        wish = request.POST['wish'],
        desc = request.POST['desc'],
        wished_by = me,
    )
    return redirect('/wishes')


def remove(request, id):
    wish = Wish.objects.get(id=id)
    wish.delete()
    return redirect('/wishes')

def edit_wish(request, id):
    wish = Wish.objects.get(id=id)
    me = User.objects.get(id=request.session['current_user'])
    wish.wish = request.POST['wish']
    wish.desc = request.POST['desc']
    wish.save()
    return redirect('/wishes')

def grant_wish(request, id):
    wish = Wish.objects.get(id=id)
    wish.grant = not wish.grant
    wish.save()
    return redirect('/wishes')


def liking_wish(request, id):
    wish = Wish.objects.get(id=id)
    user = User.objects.get(id = request.session['current_user'])
    wish.liked_by.add(user)
    return redirect('/wishes')

def unliking_wish(request, id):
    wish = Wish.objects.get(id=id)
    user = User.objects.get(id = request.session['current_user'])
    wish.liked_by.remove(user)
    return redirect('/wishes')


def adding_user(request):
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    is_user_created = User.objects.filter(email = request.POST['email']).first() #if already existed will return an object
    if is_user_created:#returns true or false
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
                first_name=request.POST['first_name'], 
                last_name=request.POST['last_name'], 
                email=request.POST['email'], 
                password=hashed_pw
            )
        request.session['current_user'] = new_user.id
        return redirect('/wishes')



def login(request):
    email_check = User.objects.filter(email = request.POST['email']).first()
    if email_check:
        pw_check = bcrypt.checkpw(request.POST['password'].encode(), email_check.password.encode())
        if pw_check:
            request.session['current_user'] = email_check.id
            return redirect('/wishes')
        else:
            messages.error(request, 'Password invalid')
            return redirect('/')
    messages.error(request, 'Invalid cradential')
    return redirect('/')

