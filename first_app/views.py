from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse, JsonResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
import requests
import os
import pandas as pd
from bs4 import BeautifulSoup
from django.db.models import Avg, Max
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.clickjacking import xframe_options_exempt
from .forms import SignUpForm, AssessmentForm
from .models import Game, Assessment


#web scrapping bs4
# def get_content():
#     url = "https://www.highspeedinternet.com/in/oldenburg"
#     page = requests.get(url)

#     soup = BeautifulSoup(page.content, "html.parser")

#     results = soup.find_all('div', class_="row large-padding provider-card-main")
#     i = 0
#     listt = []

#     for result in results:
#         info = {}
#         name_tag = result.find('a')
#         if name_tag is not None:
#             name = name_tag['data-brand'].strip()
#             info['name'] = name
#         else: continue

#         speed_i = result.find('div', class_="provider-card-item small-only-text-center")
#         if speed_i is not None:
#             speed = speed_i.text.strip()
#             info['internet_speed'] = speed
#         else: continue

#         listt.append(info)

#         i += 1
#         if i == 7:
#             break

#     return listt

# @staff_member_required
# def inst_ph(request):
#     if request.method == 'POST':
#         form = Photoform(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('gallery')
#     else:
#         form = Photoform()
#     images = Photo.objects.all()
#     return render(request, 'gallery.html', {'form' : form , 'images': images})

# def download(request, ph_id):
#     ph = get_object_or_404(Photo, pk=ph_id)
#     file_path = ph.main_img.path
#     response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f'{ph.name}.{ph.main_img}')
#     return response

# #extract data using api
# def api_population(request):
#     context = {}
#     if request.method == 'POST':
#         name = request.POST.get('c_name')
#         url = f'https://api.api-ninjas.com/v1/city?name={name}'
#         resp = requests.get(url, headers={'X-Api-Key' : 'p6ajFodyV72YVTN90n9cTg==CRfTtWAFpyEeXwNN'}) 
#         data = resp.json()
#         city = data[0]['name']
#         pop = data[0]['population']
#         context['city'] = city
#         context['population'] = pop
#     return render(request, 'search_pop.html', context)


# extract data from excel using pandas 
# def exc_unem():
#     file = 'static/data/un.xlsx'
#     info = {}
#     # data = pd.read_excel(file, usecols="C,E,H")
#     for col in data:
#         info[col] = data[col].tolist()
#     return info

def game(request,pk):
    game = Game.objects.get(id=pk)
    form = AssessmentForm()
    old = Assessment.objects.filter(game=game, user=request.user).first()
    submitted = False
    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.game = game
            assessment.user = request.user
            if old:
                new_value = int(request.POST.get('value'))
                old.value = new_value
                old.save()
            else:
                assessment.save()
        else:
            form = AssessmentForm()
            if 'submitted' in request.GET:
                submitted = True

    return render(request, 'game.html', {'game' : game, 'form' : form, 'submitted' : submitted})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged In'))
            return redirect('home')
        else:
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('home')
        else:
            return redirect('home')
    else:
        return render(request, 'register.html', {'form' : form})
    
def list(request):
    user = request.user

    games = Game.objects.all()
    paginator = Paginator(games, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    if user.is_authenticated:
        assess = Assessment.objects.filter(user=user)
        list = {}
        for asse in assess:
            list[asse.game_id] = asse.game_id
        return render(request, 'list.html', {"games" : games, "list" : list, 'page_obj' : page_obj})
    else:
        return render(request, 'list.html', {"games" : games, 'page_obj' : page_obj})

def about(request):
    return render(request, 'about.html')

def user_total(request, pk):
    user = request.user
    game = Game.objects.get(id=pk)
    f_value = Assessment.objects.filter(user=user, game=game).values()
    value = f_value[0]['value']
    average = Assessment.objects.filter(game=game).aggregate(Avg('value'))
    avg = int(average['value__avg'])
    return render(request, "user_total.html", {'game' : game, 'value' : value, 'average' : avg})

def profile(request):
    user = request.user
    total = Assessment.objects.filter(user=user).count()
    max = Assessment.objects.filter(user=user).aggregate(Max('value'))
    max_a = max['value__max']
    rat = Assessment.objects.filter(user=user)
    objs = Assessment.objects.filter(user=user).order_by('-value')[:3]


    return render(request, 'profile.html', {'user' : user, 'total' : total, 'max' : max_a, 'objs' : objs, 'rating' : rat})

def gallery(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.success(request, ("Login/Register first"))
            return redirect('home')
        
    return render(request, 'gallery.html')

def game_detail(request, pk):
    game = Game.objects.get(id=pk)

    if request.user.is_authenticated:
        ratings = Assessment.objects.filter(user=request.user, game=game).values()
        try:
            value = ratings[0]['value']
        except:
            value = 'Have not Rated' 

        average = Assessment.objects.filter(game=game).aggregate(Avg('value'))
        try:
            avg = int(average['value__avg'])
        except:
            avg = 'No recordings available'
        
        return render(request, 'game_detail.html', {"game" : game, 'average' : avg, 'value' : value})
    else:
        value = 'Have not Rated'
        average = Assessment.objects.filter(game=game).aggregate(Avg('value'))
        try:
            avg = int(average['value__avg'])
        except:
            avg = 'No recordings available'

        return render(request, 'game_detail.html', {"game" : game, 'average' : avg, 'value' : value})

@xframe_options_exempt
def game_detail_iframe(request, pk):
    game = Game.objects.get(id=pk)
    average = Assessment.objects.filter(game=game).aggregate(Avg('value'))
    ratings = Assessment.objects.filter(user=request.user, game=game).values()
    value = ratings[0]['value']
    try:
        avg = int(average['value__avg'])
    except:
        avg = 'No user rating on this game yet'
    return render(request, 'gd_iframe.html', {"game" : game, 'average' : avg, 'value' : value})

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        games = Game.objects.filter(name__contains=searched)
        return render(request, 'searched_games.html', {'games' : games})
    else:
        return render(request, 'searched_games.html', {'games' : games})

def home(request):
    latest = Assessment.objects.order_by('-id')[:10]
    if request.user.is_authenticated:
        user = request.user
        obj = Assessment.objects.filter(user=user).order_by('-id')[:8]
        if obj.exists():
            for a in obj:
                gamer = a.game
                img = gamer.image
        
            return render(request, 'home.html', {'obj' : obj, 'img' : img, 'game' : gamer, 'latest' : latest})
        else:
            return render(request, 'home.html', {"latest" : latest})
    else:
        return render(request, 'home.html', {"latest" : latest})