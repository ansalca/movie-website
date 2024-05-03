from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('', views.movie, name='movies'),
    path('register/', views.reg, name='register'),
    path('register_action/', views.registeraction, name='register_action'),
    path('login/', views.login, name='login'),
    path('login_action/', views.userloginaction, name='login_action'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('add_movie/', views.add_movie, name='addmovie'),
    path('add_movie_action/', views.add_movie_action, name='add_movie_action'),
    path('category/<str:category_name>/', views.category_movies, name='category_movies'),
]

# # Define the URL patterns
# urlpatterns = [
#     url(r'^$', index, name='index'),
#     url(r'^register/$', register, name='register'),
#     url(r'^login/$', login, name='login'),
#     url(r'^profile/$', profile, name='profile'),
#     url(r'^add_movie/$', add_movie, name='add_movie'),
#     url(r'^admin_panel/$', admin_panel, name='admin_panel'),
# ]
