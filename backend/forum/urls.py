from django.urls import path
from forum.views import (
    ForumRegisterView,
    ForumListView,
    SubscribeView,
    ForumDetailView,
    ForumEditView,
    ForumDeleteView
)
 

urlpatterns = [
    path('register/',ForumRegisterView.as_view(), name='forum_register'),
    path('list/', ForumListView.as_view(), name='forum_list'),
    path('edit/<slug:slug>/',ForumEditView.as_view(), name='forum_edit'),
    path('delete/<slug:slug>/', ForumDeleteView.as_view(), name='forum_delete'),
    path('subscribe/<slug:slug>/', SubscribeView.as_view(), name='forum_subscribe'),
    path('detail/<slug:slug>/', ForumDetailView.as_view(), name='forum_detail')
]
