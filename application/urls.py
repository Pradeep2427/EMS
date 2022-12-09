from . import views
from django.urls import path

# application urls --- This file has to be included in main urls file

urlpatterns = [
    path('delete-Event',views.delete_Event, name='delete_Event'),
    path('add-summary',views.add_Summary, name='add_Summary'),
    path('event-summary',views.event_Summary, name='event_Summary'),
    path('add-event',views.add_Event, name='add_Event'),
    path('Event-Update',views.event_Update, name='event_Update'),
    path('home',views.home, name='home'),
    path('Login', views.check_Cred, name='check_Cred'),
    path('',views.login,name='login')
]