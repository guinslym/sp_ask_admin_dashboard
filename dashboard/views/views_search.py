from lh3.api import *
from dashboard.utils.utils import (
    soft_anonimyzation, operatorview_helper, Chats, retrieve_transcript, search_chats
)
from datetime import datetime, timedelta, timezone
from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.http import HttpResponse, HttpResponseNotFound
from pprint import pprint as print
from django.contrib import messages
import random


from datetime import datetime
from datetime import timezone
import json

from dateutil.parser import parse

from django.http import JsonResponse

from dashboard.utils.ask_schools  import   find_school_by_operator_suffix, find_queues_from_a_school_name, find_school_by_queue_or_profile_name

import warnings
warnings.filterwarnings("ignore")

"""
List of VIEW FUNCTIONS/CLASSES
SearchProfileResultsView
get_this_profile
get_transcript
get_chats_for_this_school_using_an_username
get_chats_for_this_school_using_this_queue_name
get_chats_from_this_queue_using_only_the_queue_name
get_chats_for_this_user
get_chats_for_this_queue
get_chats_from_yesterday
get_chats_from_yesterday_from_mentees
"""


class SearchProfileResultsView(TemplateView):
    template_name = "results/profile.html"

    @csrf_exempt
    def get_context_data(self, **kwargs):
        context = super(SearchProfileResultsView, self).get_context_data(**kwargs)
        context['title'] = "Profile"
        search_value = self.request.GET.get('queue_id')
        
        client = Client()
        profile = client.one('profiles', int(search_value)).get()
        context['profile'] = profile['content']
        context['title'] = profile['name']
        context["queues"] = client.all('queues').get_list()
        context['standalone_link'] = "https://ca.libraryh3lp.com/dashboard/profiles/" + str(int(search_value)) + "?standalone=true"

        return context

def get_this_profile(request, *args, **kwargs):
    queue_id = kwargs.get('queue_id', None)
    queue_id = int(queue_id)
    client = Client()
    queues = client.all('queues').get_list()
    title = "Profile"
    profile = None
    if queue_id: 
        profile_api = client.one('profiles', int(queue_id)).get()
        profile = profile_api['content']
        title = profile_api.get('name', None)
        standalone_link = "https://ca.libraryh3lp.com/dashboard/profiles/" + str(int(queue_id)) + "?standalone=true"
        
        if request.is_ajax():
            return JsonResponse(profile, safe=False)
        return render(request, 'results/profile.html', {'profile':profile, 'title':title, 'standalone_link':standalone_link, 'queues':queues})
    if request.is_ajax():
        return JsonResponse(queues, safe=False)
    return render(request, 'results/profile.html', {'queues':queues, 'title':title, 'profile':profile})





def get_chats_for_this_school_using_an_username(request, *args, **kwargs):
    client = Client()
    username = kwargs.get('username', None)
    school_name = find_school_by_operator_suffix(username).lower()
    queues_from_school = find_queues_from_a_school_name(school_name)
    print("username: {0}".format(username))
    print("school_name: {0}".format(school_name))
    query = {
        'query': {
            'queue': queues_from_school,
            'from': '2021-01-01',
            'to': '2021-12-31'
        },
        'sort': [
            {'started': 'descending'}
        ]
    }
    queue_chats = client.api().post('v4', '/chat/_search', json = query)
    chats = soft_anonimyzation(queue_chats)
    today = datetime.today()
    current_year = today.year
    total_chats = len(chats)

    heatmap = [parse(chat.get('started')).replace(tzinfo=timezone.utc).timestamp() for chat in chats]
    counter=  {x:heatmap.count(x) for x in heatmap}
    heatmap_chats = json.dumps(counter)  
    #print(chats)
    chats = [Chats(chat) for chat in chats]
    if request.is_ajax():
        return JsonResponse({'object_list':chats,
                    'heatmap_chats':heatmap_chats, 'username':school_name, 
                    "current_year":current_year, "total_chats":total_chats}, 
                    safe=False)
    return render(request, 'results/chats.html', {
                    'object_list':chats,
                    'heatmap_chats':heatmap_chats, 'username':school_name, 
                    "current_year":current_year, "total_chats":total_chats})


def get_chats_for_this_school_using_this_queue_name(request, *args, **kwargs):
    client = Client()
    queue_name = kwargs.get('queue_name', None)
    school_name = find_school_by_queue_or_profile_name(queue_name)
    queues_from_school = find_queues_from_a_school_name(school_name)
    
    print("queue_name: {0}".format(queue_name))
    print("school_name: {0}".format(school_name))
    query = {
        'query': {
            'queue': queues_from_school,
            'from': '2021-01-01',
            'to': '2021-12-31'
        },
        'sort': [
            {'started': 'descending'}
        ]
    }
    #breakpoint()
    queue_chats = client.api().post('v4', '/chat/_search', json = query)
    chats = soft_anonimyzation(queue_chats)
    today = datetime.today()
    current_year = today.year
    total_chats = len(chats)

    heatmap = [parse(chat.get('started')).replace(tzinfo=timezone.utc).timestamp() for chat in chats]
    counter=  {x:heatmap.count(x) for x in heatmap}
    heatmap_chats = json.dumps(counter)  
    #print(chats)
    chats = [Chats(chat) for chat in chats]
    if request.is_ajax():
        return JsonResponse({'object_list':chats,
                    'heatmap_chats':heatmap_chats, 'username':school_name, 
                    "current_year":current_year, "total_chats":total_chats}, 
                    safe=False)
    return render(request, 'results/chats_from_queues.html', {
                    'object_list':chats,
                    'heatmap_chats':heatmap_chats, 'username':school_name, 
                    "current_year":current_year, "total_chats":total_chats})


def get_chats_from_this_queue_using_only_the_queue_name(request, *args, **kwargs):
    client = Client()
    queue_name = kwargs.get('queue_name', None)
    
    print("queue_name: {0}".format(queue_name))
    query = {
        'query': {
            'queue': [queue_name],
            'from': '2021-01-01',
            'to': '2021-12-31'
        },
        'sort': [
            {'started': 'descending'}
        ]
    }
    #breakpoint()
    queue_chats = client.api().post('v4', '/chat/_search', json = query)
    chats = soft_anonimyzation(queue_chats)
    today = datetime.today()
    current_year = today.year
    total_chats = len(chats)

    heatmap = [parse(chat.get('started')).replace(tzinfo=timezone.utc).timestamp() for chat in chats]
    counter=  {x:heatmap.count(x) for x in heatmap}
    heatmap_chats = json.dumps(counter)  
    #print(chats)
    chats = [Chats(chat) for chat in chats]
    if request.is_ajax():
        return JsonResponse({'object_list':chats,
                    'heatmap_chats':heatmap_chats, 'username':queue_name, 
                    "current_year":current_year, "total_chats":total_chats}, 
                    safe=False)
    return render(request, 'results/chats.html', {
                    'object_list':chats,
                    'heatmap_chats':heatmap_chats, 'username':queue_name, 
                    "current_year":current_year, "total_chats":total_chats})


def get_chats_for_this_user(request, *args, **kwargs):
    client = Client()
    username = kwargs.get('username', None)
    query = {
        'query': {
            'operator': [username],
            'from': '2019-01-01',
            'to': '2021-12-31'
        },
        'sort': [
            {'started': 'descending'}
        ]
    }
    chats_from_users = client.api().post('v4', '/chat/_search', json = query)
    chats = soft_anonimyzation(chats_from_users)
    
    today = datetime.today()
    current_year = today.year
    total_chats = len(chats_from_users)

    assignments = operatorview_helper(username)
    heatmap = [parse(chat.get('started')).replace(tzinfo=timezone.utc).timestamp() for chat in chats]
    counter=  {x:heatmap.count(x) for x in heatmap}
    heatmap_chats = json.dumps(counter)  
    if request.is_ajax():
        return JsonResponse({'chats':chats, "assignments":assignments, 
                            'heatmap_chats':heatmap_chats , 'username':username,
                             "current_year":current_year, "total_chats":total_chats }, safe=False)
    chats = [Chats(chat) for chat in chats]
    return render(request, 'results/chats.html', 
                    {'object_list':chats, "assignments":assignments, 
                    'heatmap_chats':heatmap_chats, 'username':username, 
                    "current_year":current_year, "total_chats":total_chats })


def get_chats_for_this_queue(request, *args, **kwargs):
    client = Client()
    queue = kwargs.get('queue_name', None)
    query = {
        'query': {
            'queue': [queue],
            'from': '2021-01-01',
            'to': '2021-01-19'
        },
        'sort': [
            {'started': 'descending'}
        ]
    }
    queue_chats = client.api().post('v4', '/chat/_search', json = query)
    chats = soft_anonimyzation(queue_chats)
    return JsonResponse(chats, safe=False)


def get_chats_of_today(request, *args, **kwargs):
    client = Client()
    today = datetime.today()
    
    query = {
        'query': {
            'from': today.strftime('%Y-%m-%d')
        },
        'sort': [
            {'started': 'ascending'}
        ]
    }
    chats_from_users = client.api().post('v4', '/chat/_search', json = query)
    chats = soft_anonimyzation(chats_from_users)

    heatmap = [parse(chat.get('started')).replace(tzinfo=timezone.utc).timestamp() for chat in chats]
    counter=  {x:heatmap.count(x) for x in heatmap}
    heatmap_chats = json.dumps(counter)
    username= "Yesterday"  
    #filter chats from yesteday only
    chats = [Chats(chat) for chat in chats]

    #return JsonResponse(chats, safe=False)
    if request.is_ajax():
        return JsonResponse(chats, safe=False)
    return render(request, "results/chats.html", {'object_list':chats, 'heatmap_chats':heatmap_chats,
                'username':username, "current_year":"Yesterday", "total_chats":len(chats)})


def get_chats_from_yesterday(request, *args, **kwargs):
    client = Client()
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    
    query = {
        'query': {
            'from': yesterday.strftime('%Y-%m-%d')
        },
        'sort': [
            {'started': 'ascending'}
        ]
    }
    #chats_from_users = client.api().post('v4', '/chat/_search', json = query)
    chats_from_users, content_range = search_chats(client, query, chat_range=(0, 350))
    chats = soft_anonimyzation(chats_from_users)

    heatmap = [parse(chat.get('started')).replace(tzinfo=timezone.utc).timestamp() for chat in chats]
    counter=  {x:heatmap.count(x) for x in heatmap}
    heatmap_chats = json.dumps(counter)
    username= "Yesterday"  
    #filter chats from yesteday only
    chats = [chat for chat in chats if  yesterday.strftime('%Y-%m-%d') == parse(chat.get('started')).strftime('%Y-%m-%d') ]
    chats = [Chats(chat) for chat in chats]

    #return JsonResponse(chats, safe=False)
    if request.is_ajax():
        return JsonResponse(chats, safe=False)
    return render(request, "results/chats.html", {'object_list':chats, 'heatmap_chats':heatmap_chats,
                'username':username, "current_year":"Yesterday", "total_chats":len(chats)})


def get_chats_from_yesterday_from_mentees(request, *args, **kwargs):
    client = Client()
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    
    query = {
        'query': {
            'from': yesterday.strftime('%Y-%m-%d')
        },
        'sort': [
            {'started': 'descending'}
        ]
    }
    #chats_from_users = client.api().post('v4', '/chat/_search', json = query)
    chats_from_users, content_range = search_chats(client, query, chat_range=(0, 100))
    chats = soft_anonimyzation(chats_from_users)
    chat_picked_up_by_mentees = list()
    for chat in chats:
        if chat.get('accepted'):
            if "_int" in chat.get('operator'):
                chat_picked_up_by_mentees.append(chat) 
    chats = chat_picked_up_by_mentees

    heatmap = [parse(chat.get('started')).replace(tzinfo=timezone.utc).timestamp() for chat in chats]
    counter=  {x:heatmap.count(x) for x in heatmap}
    heatmap_chats = json.dumps(counter)
    username= "Mentees"  
    #filter chats from yesteday only
    chats = [chat for chat in chats if  yesterday.strftime('%Y-%m-%d') == parse(chat.get('started')).strftime('%Y-%m-%d') ]
    chats = [Chats(chat) for chat in chats]

    #return JsonResponse(chats, safe=False)
    if request.is_ajax():
        return JsonResponse(chats, safe=False)
    return render(request, "results/chats.html", {'object_list':chats, 'heatmap_chats':heatmap_chats,
                'username':username, "current_year":"Yesterday", "total_chats":len(chats)})




def get_chats_from_yesterday_sample_size(request, *args, **kwargs):
    client = Client()
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    
    query = {
        'query': {
            'from': yesterday.strftime('%Y-%m-%d')
        },
        'sort': [
            {'started': 'ascending'}
        ]
    }
    chats_from_users, content_range = search_chats(client, query, chat_range=(0, 350))
    chats_from_users = random.sample(chats_from_users, int(50*0.20))
    chats = soft_anonimyzation(chats_from_users)

    heatmap = [parse(chat.get('started')).replace(tzinfo=timezone.utc).timestamp() for chat in chats]
    counter=  {x:heatmap.count(x) for x in heatmap}
    heatmap_chats = json.dumps(counter)
    username= "Yesterday"  
    #filter chats from yesteday only
    chats = [chat for chat in chats if  yesterday.strftime('%Y-%m-%d') == parse(chat.get('started')).strftime('%Y-%m-%d') ]
    chats = [Chats(chat) for chat in chats]

    #return JsonResponse(chats, safe=False)
    if request.is_ajax():
        return JsonResponse(chats, safe=False)
    return render(request, "results/chats.html", {'object_list':chats, 'heatmap_chats':heatmap_chats,
                'username':username, "current_year":"Yesterday", "total_chats":len(chats)})

def get_chat_for_date_range(request, *args, **kwargs):
    start_date = request.GET.get('start_date','')
    end_date = request.GET.get('end_date','')
    if start_date and end_date:
        if start_date:
            start_date_with_time = parse(start_date)
        
        if end_date:
            end_date_with_time = parse(end_date)

        if end_date < start_date:
            messages.warning(request, 'The End_date should be greater than the Start Date') 
            return render(request, "results/search_between_date.html", {'object_list':None})
        client = Client()
        chats = client.chats()
        to_date = str(end_date_with_time.year) + "-" + '{:02d}'.format(end_date_with_time.month)  + "-" + str(end_date_with_time.day)
        all_chats = chats.list_day(year=start_date_with_time.year, month=start_date_with_time.month, day=start_date_with_time.day, to=to_date)

        #return JsonResponse(chats, safe=False)
        chats = [Chats(chat) for chat in all_chats]
        selected_chats= list()
        for chat in chats:
            if (parse(chat.started) >= start_date_with_time) and (parse(chat.ended) <= end_date_with_time):
                selected_chats.append(chat)
        return render(request, "results/search_between_date.html", {'object_list':selected_chats})
    return render(request, "results/search_between_date.html", {'object_list':None})


def search_chats_within_2_hours(request, *args, **kwargs):
    client = Client()
    chat_id = int(kwargs.get('chat_id', None))
    chat = client.one('chats', chat_id).get()

    
    if chat:
        start_date = parse(chat.get('started')) 
        chats = client.chats()
        chats = chats.list_day(start_date.year, start_date.month, start_date.day)

        chat_within_2_hours = list()
        for chat in chats:
            started = parse(chat.get('started'))
            #print("{0} > {1} < {2}".format(started-timedelta(minutes=60), start_date , started+timedelta(minutes=60)))
            if (started-timedelta(60) > start_date < started+timedelta(60)):
                chat_within_2_hours.append(chats)

        #print(chat_within_2_hours)
        chats = None
        if chat_within_2_hours:
            chats = soft_anonimyzation(chat_within_2_hours)

        return JsonResponse(chats, safe=False)
    return JsonResponse(None, safe=False)

@csrf_exempt
def search_chats_with_this_guestID(request, *args, **kwargs):
    guest_id = request.POST.get('guest_id',None)
    chats = None
    if guest_id:
        if "@" in guest_id:
            pass
        else:
            guest_id = guest_id + '*'
        query = {
            'query': {
                'guest': [guest_id],
            },
            'sort': [
                {'started': 'descending'}
            ]
        }
        client = Client()
        chats = client.api().post('v4', '/chat/_search', json = query)
        chats = soft_anonimyzation(chats)
        chats = [Chats(chat) for chat in chats]
        return render(request, "results/search_guest.html", {'object_list':chats, 'guest_id':guest_id})
    return render(request, "results/search_guest.html", {'object_list':None})

class SearchGuestResultsView(TemplateView):
    template_name = "results/search_guest.html"
