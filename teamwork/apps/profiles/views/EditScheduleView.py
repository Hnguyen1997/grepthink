# Django Imports
from __future__ import print_function
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.http import HttpResponse
# Model Imports
from teamwork.apps.profiles.models import Profile
from django.http import HttpResponseRedirect

# Model Imports
from teamwork.apps.profiles.models import Profile, Events
from teamwork.apps.projects.models import dayofweek
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.discovery import build
from itertools import *

# Form Imports

# View Imports

# Other Imports
import json
import httplib2
import os
import datetime

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
flags = tools.argparser.parse_args([])

@login_required
def edit_schedule(request, username):
    """
    Public method that takes a request and a username.
    Gets a list of 'events' from a calendar and stores the event as an array of tuples
    Redners profiles/edit_calendar.html
    """

    user = get_object_or_404(User, username=username)
    page_name = "Edit Schedule"
    page_description = "Edit %s's Schedule"%(user.username)
    title = "Edit Schedule"
    profile = Profile.objects.get(user=user)
    
    #gets current avaliability
    readable = ""
    if profile.jsonavail:
        jsonDec = json.decoder.JSONDecoder()
        readable = jsonDec.decode(profile.jsonavail)

    meetings = mark_safe(profile.jsonavail)

    return render(request, 'profiles/edit_schedule.html', {'page_name' : page_name, 'page_description': page_description, 'title': title, 'json_events' : meetings})

@csrf_exempt
def save_event(request, username):
    #grab profile for the current user
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.POST.get('Clear'):
            profile.jsonavail = ""
            profile.save()

            # If user already has a schedule, delete it
            if profile.avail.all() is not None: profile.avail.all().delete()

            profile.save()
            return HttpResponse("Schedule Cleared")

        # List of events as a string (json)
        jsonEvents = request.POST.get('jsonEvents')
        print(jsonEvents)
        # Load json event list into a python list of dicts
        event_list = json.loads(jsonEvents)

        profile.jsonavail = json.dumps(event_list)
        profile.save()

        # If user already has a schedule, delete it
        if profile.avail.all() is not None: profile.avail.all().delete()

        # For each event
        for event in event_list:
            # Create event object
            busy = Events()

            # Get data
            #function assumes start day and end day are the same
            day = event['start'][8] + event['start'][9]
            day = int(day)
            s_hour = event['start'][11] + event['start'][12]
            s_minute = event['start'][14] + event['start'][15]

            s_hour = int(s_hour)
            s_minute = int(s_minute)

            e_hour = event['end'][11] + event['end'][12]
            e_minute = event['end'][14] + event['end'][15]
            e_hour = int(e_hour)
            e_minute = int(e_minute)

            # Assign data
            busy.day = dayofweek(day)
            busy.start_time_hour = s_hour
            busy.start_time_min = s_minute
            busy.end_time_hour = e_hour
            busy.end_time_min = e_minute

            # Save event
            busy.save()

            profile.avail.add(busy)
            profile.save()


        return HttpResponse("Schedule Saved")
        #return HttpResponse(json.dumps({'eventData' : eventData}), content_type="application/json")

    return HttpResponse("Failure")

@login_required
def import_schedule(request,username):
    #otain credentials if it's non-existed
    store = Storage('storage.json')
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        credentials = tools.run_flow(flow, store,flags)
        print('Storing credentials to' + str(store))
    

    http = credentials.authorize(httplib2.Http())
    service = build('calendar', 'v3', http=http)

    result_events=get_calendar(credentials,service) #obtain list of calendar events
    
    events_list=[]
    for event in result_events:         # append calendar information into the list with corrected format for FullCalendar
        title= event['summary']
        if(event['start'].get('dateTime') is not None):             #get timed event from Google Calendar
            start=event['start'].get('dateTime')
            end=event['end'].get('dateTime')
            this_event={'title':title,'start':start,'end':end}
            print(this_event)
        elif(event['start'].get('date') == event['end'].get('date')):  #get all-day event from Google Calendar
            start=event['start'].get('date')
            this_event={'title':title,'start':start}
            print(this_event)
        else:
            start=event['start'].get('date')                        #get multi-day spanned event from Google Calendar
            end=event['end'].get('date')
            this_event={'title':title,'start':start,'end':end}                                                     
            print(this_event)
            
        events_list.append(this_event)                              #add all events into one list


    print(events_list)  
    
    profile = Profile.objects.get(user=request.user)        
    profile.jsonavail = json.dumps(events_list)     #save calendar events into profile.jsonavail
    profile.save()

    return HttpResponseRedirect("/")
 
def get_calendar(credentials,service):

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=250, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    return events


@login_required
def export_schedule(request,username):
    #obtain credentials if it's non-existed
    store = Storage('storage.json')
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        credentials = tools.run_flow(flow, store,flags)
        print('Storing credentials to' + str(store))
    
    http = credentials.authorize(httplib2.Http())
    service = build('calendar', 'v3', http=http)

    profile = Profile.objects.get(user=request.user)
    readable=""
    if profile.jsonavail:
        jsonDec = json.decoder.JSONDecoder()
        readable = jsonDec.decode(profile.jsonavail)

    #put data from profile.jsonavail into google calendar format and send
    EVENT={'summary':'','start':{'dateTime':''},'end':{'dateTime':''}}
    for event in readable:
        EVENT['summary']=event['title']
        EVENT['start']['dateTime']=event['start']
        EVENT['end']['dateTime']=event['end']
        print(EVENT['start'],EVENT['end'])
        send=service.events().insert(calendarId='primary',sendNotifications=True,body=EVENT).execute()

    return HttpResponseRedirect("/")


    