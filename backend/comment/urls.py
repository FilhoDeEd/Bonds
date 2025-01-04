from django.urls import path
from comment.views import (
    CommentRegisterView,
    CommentEditView,
    CommentDeleteView,
    CommentListView
)

urlpatterns = [
    path('register/',CommentRegisterView.as_view(), name='comment_register'),
    path('edit/<int:comment_id>/',CommentEditView.as_view(), name='comment_edit'),
    path('delete/<int:comment_id>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('list/<int:forum_id>/', CommentListView.as_view(), name='comment-list'),
]