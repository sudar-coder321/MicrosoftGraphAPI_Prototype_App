from django.urls import path

from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('signin', views.sign_in, name='signin'),
  path('callback', views.callback, name='callback'),
  path('signout', views.sign_out, name='signout'),
  path('calendar', views.calendar, name='calendar'),
  path('userinfo',views.user_info,name='userinfo'),
  path('groupinfo',views.get_users_by_group,name='groupinfo')
]