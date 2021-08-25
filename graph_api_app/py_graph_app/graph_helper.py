from requests_oauthlib import OAuth2Session
import json
graph_url = 'https://graph.microsoft.com/v1.0/'

def get_current_user(token):
  graph_client = OAuth2Session(token=token)
  # Send GET to /me
  user = graph_client.get('{0}/me'.format(graph_url))
  # Return the JSON result
  return user.json()

def get_calendar_events(token):
  graph_client = OAuth2Session(token=token)

  # Configure query parameters to
  # modify the results
  query_params = {
    '$select': 'subject,organizer,start,end',
    '$orderby': 'createdDateTime DESC'
  }

  # Send GET to /me/events
  events = graph_client.get('{0}/me/events'.format(graph_url), params=query_params)
  # Return the JSON result
  return events.json()


def get_group_members(token):
  graph_client = OAuth2Session(token=token)
  
  group_id='32fe7bdc-0c91-4be5-ad1e-0690b6db13e4'

  groups=graph_client.get('{0}/groups/{1}/members'.format(graph_url,group_id))
  
  return groups.json()
  