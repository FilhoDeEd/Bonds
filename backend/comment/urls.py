from django.urls import path
from comment.views import (
    CommentRegisterView,
)

urlpatterns = [
    path('register/',CommentRegisterView.as_view(), name='comment_register'),
    
]