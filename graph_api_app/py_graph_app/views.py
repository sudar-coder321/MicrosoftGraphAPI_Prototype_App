from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from py_graph_app.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from py_graph_app.graph_helper import get_current_user, get_calendar_events,get_group_members
import dateutil.parser

def home(request):
    context = initialize_context(request)

    return render(request, 'py_graph_app/home.html', context)

def initialize_context(request):
    context = {}

  # Check for any errors in the session
    error = request.session.pop('flash_error', None)

    if error != None:
        context['errors'] = []
        context['errors'].append(error)

  # Check for user in the session
    context['user'] = request.session.get('user', {'is_authenticated': False})
    return context

def sign_in(request):
      # Get the sign-in URL
  sign_in_url, state = get_sign_in_url()
  # Save the expected state so we can validate in the callback
  request.session['auth_state'] = state
  # Redirect to the Azure sign-in page
  return HttpResponseRedirect(sign_in_url)

def callback(request):
      # Get the state saved in session
  expected_state = request.session.pop('auth_state', '')
  # Make the token request
  token = get_token_from_code(request.get_full_path(), expected_state)

  # Get the user's profile
  user = get_current_user(token)

  # Save token and user
  store_token(request, token)
  store_user(request, user)

  return HttpResponseRedirect(reverse('home'))

def sign_out(request):
      # Clear out the user and token
  remove_user_and_token(request)

  return HttpResponseRedirect(reverse('home'))

def calendar(request):
  context = initialize_context(request)

  token = get_token(request)

  events = get_calendar_events(token)

  if events:
    # Convert the ISO 8601 date times to a datetime object
    # This allows the Django template to format the value nicely
    for event in events['value']:
      event['start']['dateTime'] = dateutil.parser.parse(event['start']['dateTime'])
      event['end']['dateTime'] = dateutil.parser.parse(event['end']['dateTime'])

    context['events'] = events['value']

  return render(request, 'py_graph_app/calendar.html', context)

def user_info(request):
  context = initialize_context(request)
  
  token = get_token(request)
  
  user=get_current_user(token) 
  context['user']= user
  return render(request,'py_graph_app/userinfo.html',context)

def get_users_by_group(request):
  context=initialize_context(request)
  
  token=get_token(request)
     
  groups=get_group_members(token)

  context['users'] = groups['value']
  
  return render(request,'py_graph_app/groupinfo.html',context)
  
