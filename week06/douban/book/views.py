from django.shortcuts import render, HttpResponse

# Create your views here.
from django.db.models import Avg
from .models import T1


def book(request):
    condtions = {'n_star__gt': 3}
    comments = T1.objects.filter(**condtions)
    return render(request, 'index.html', locals())
