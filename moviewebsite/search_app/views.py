from django.db.models import Q
from django.shortcuts import render

from user.models import Movie


# Create your views here.
def Searchresult(request):
    movie = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        movie = Movie.objects.all().filter(Q(title__contains=query))
        return render(request, 'search.html', {'query': query, 'movie': movie})
