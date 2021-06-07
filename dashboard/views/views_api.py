from django.http import Http404

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound
from django.http import JsonResponse
from django.shortcuts import render

import datetime

from lh3.api import *
from dashboard.utils import utils

def get_users(request):
    client = Client()
    client.set_options(version = 'v1')
    users = client.all('users').get_list()
    if request.is_ajax():
        return JsonResponse(users, safe=False)
    return render(request, 'results/operators.html', {'object_list':users})

def get_queues(request):
    client = Client()
    client.set_options(version = 'v1')
    queues = client.all('queues').get_list()
    if request.is_ajax():
        return JsonResponse(queues, safe=False)
    return render(request, 'results/queues.html', {'object_list':queues})
    #path('queues/', GetListOfQueues.as_view(), name='Get list of Queues'),

def get_profiles(request, *args, **kwargs):
    queue_id = kwargs.get('queue_id', None)
    client = Client()
    queues = client.all('queues').get_list()
    title = "Profile"
    profile = None
    if request.method == 'GET':
        if request.is_ajax():
            return JsonResponse(profile, safe=False)
        return render(request, 'results/profile.html', {'queues':queues, 'title':title, 'profile':profile})
    if queue_id: 
        profile = client.one('profiles', int(queue_id)).get()
        profile = profile['content']
        title = profile['name']
        standalone_link = "https://ca.libraryh3lp.com/dashboard/profiles/" + str(int(queue_id)) + "?standalone=true"
        
        if request.is_ajax():
            return JsonResponse(profile, safe=False)
        return render(request, 'results/profile.html', {'profile':profile, 'title':title, 'standalone_link':standalone_link})
    if request.is_ajax():
        return JsonResponse(queues, safe=False)
    return render(request, 'results/profile.html', {'queues':queues, 'title':title, 'profile':profile})

#TODO clean template html remove console error.


