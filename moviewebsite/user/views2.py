from django.contrib import messages, auth
from django.contrib.auth.backends import UserModel
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse

from .models import Movie, Category


# Create your views here.


def reg(request):
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
                return redirect(reverse('user:register'))
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                return redirect(reverse('user:register'))
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=password)
                user.save()
                messages.success(request, 'Account created successfully')
                return redirect(reverse('user:login'))
        else:
            messages.info(request, "Password not matching")
            return redirect(reverse('user:register'))
    return render(request, 'Register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        try:
            auth.login(request, user)
            movies = Movie.objects.all()
            category = Category.objects.all()
            logged_in = user
            return render(request, 'movies.html', {'movie_list': movies, 'category': category, 'user': logged_in})
        except:
            messages.error(request, 'invalid credentials')
            return redirect('Login')
    return render(request, 'Login.html')


def userview(request):
    data_list = UserModel.objects.all()
    return render(request, "adminuserview.html", {'data': data_list})


def movie(request):
    movies = Movie.objects.all()
    category = Category.objects.all()
    return render(request, 'movies.html', {'movie_list': movies, 'category': category})


def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


def add_movie(request):
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
        return redirect(reverse('user:movie'))
    return render(request, 'add.html', {'category': category})


def admin_panel(request):
    if request.method == 'POST':
        uname = request.POST['adminname']
        passwd = request.POST['adminpasswd']
        if uname == 'admin' and passwd == 'admin':
            return render(request, "adminuserview.html")
        else:
            messages.warning(request, "invalied Credentials")
            return render(request, "adminlogin.html")
    return render(request, "adminlogin.html")

# views.py
def add_to_favorites(request, item_id):
    if request.user.is_authenticated:
        # Create a favorite object for the current user and item
        favorite = Favorite(user=request.user, item_id=item_id)
        favorite.save()
        return render(request, 'movies.html')
    else:
        return render(request, 'Login.html')
# models.py
class Favorite(models.Model):
    user = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # Add a ForeignKey to the item being favorited
    # For example, if you're favoriting movies:
    # movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
# urls.py
    path('add_to_favourites/', views.add_to_favorites, name='add_to_favorites'),

#                     <a href="{% url 'user:add_to_favorites' item_id=i.id %}" class="btn btn-dark mt-2">Add to Favourites</a>