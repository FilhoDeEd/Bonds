from django.urls import path
from forum.views import (
    ForumRegisterView,
    ForumListView,
    SubscribeView,
    UnsubscribeView,
    ForumDetailView,
    ForumEditView,
    ForumDeleteView,
    EventRegisterView,
    EventDetailView,
    EventEditView,
    ReviewRegisterView


)
 

urlpatterns = [
    ##register de forum
    path('register/',ForumRegisterView.as_view(), name='forum_register'), 
    ##list de forum e evento
    path('list/', ForumListView.as_view(), name='forum_list'),  
    ##edit de forum         
    path('edit/<slug:slug>/',ForumEditView.as_view(), name='forum_edit'),
    ##delete de forum e evento
    path('delete/<slug:slug>/', ForumDeleteView.as_view(), name='forum_delete'),
    ##detail de forum 
    path('detail/<slug:slug>/', ForumDetailView.as_view(), name='forum_detail'),
    ##register de subscriber
    path('subscribe/<slug:slug>/', SubscribeView.as_view(), name='forum_subscribe'),
    ##delete de subscriber
    path('unsubscribe/<slug:slug>/', UnsubscribeView.as_view(), name='forum_unsubscribe'),
    ##register de evento
    path('event/register/',EventRegisterView.as_view(), name='event_register'),
    ##edit de evento
    path('event/edit/<slug:slug>/',EventEditView.as_view(), name='event_edit'),
    ##detail de evento
    path('event/detail/<slug:slug>/', EventDetailView.as_view(), name='event_detail'),
    ##register de review
    path('review/register/',ReviewRegisterView.as_view(), name='review_register'),
    ##edit de review

    ##delete de review
    


]
