from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from .forms import ProfileForm
from .models import Movie, Category


def reg(request):
    return render(request, 'Register.html')


def registeraction(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('password1')
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken")
                return render(request, 'Register.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                return render(request, 'Register.html')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=password)
                user.save()
                messages.success(request, 'Account created successfully')
                movies = Movie.objects.all()
                category = Category.objects.all()
                return render(request, 'movies.html', {'movie_list': movies, 'category': category})
        else:
            messages.info(request, "Password not matching")
            return render(request, 'Register.html')
    return render(request, 'Register.html')


def login(request):
    return render(request, 'Login.html')


def userloginaction(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        try:
            auth.login(request, user)
            movies = Movie.objects.all()
            category = Category.objects.all()
            return render(request, 'movies.html', {'movie_list': movies, 'category': category})
        except:
            messages.error(request, 'invalid credentials')
            return render(request, 'Login.html')
    return render(request, 'Login.html')


def movie(request):
    movies = Movie.objects.all()
    category = Category.objects.all()
    return render(request, 'movies.html', {'movie_list': movies, 'category': category})


def profile(request):
    return render(request, 'profile.html')


def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return render(request, 'profile.html')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'editprofile.html', {'form': form})


def add_movie(request):
    category = Category.objects.all()
    return render(request, 'add.html', {'category': category})


def add_movie_action(request):
    category = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        poster = request.FILES['img']
        description = request.POST.get('description')
        release_date = request.POST.get('release_date')
        actors = request.POST.get('actors')
        category = request.POST.get('category')
        category_instance = Category.objects.get(name=category)
        youtube_trailer_link = request.POST.get('youtube_trailer_link')

        movie = Movie(title=title, poster=poster, description=description, release_date=release_date, actors=actors,
                      category=category_instance, youtube_trailer_link=youtube_trailer_link)
        movie.save()
        return redirect(reverse('user:movies'))
    return render(request, 'add.html')

def category_movies(request, category_name):
    categry = Category.objects.get(name=category_name)
    movies = Movie.objects.filter(category=categry)
    return render(request, 'category_movies.html', {'categry': categry, 'movies': movies})