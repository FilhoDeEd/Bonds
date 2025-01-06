from django.urls import path
from comment.views import (
    CommentRegisterView,
    CommentEditView,
    CommentDeleteView,
    CommentListView,
    CommentLikeView,
    CommentDislikeView,
    CommentLikeDeleteView
)

urlpatterns = [
    path('register/',CommentRegisterView.as_view(), name='comment_register'),
    path('edit/<int:comment_id>/',CommentEditView.as_view(), name='comment_edit'),
    path('delete/<int:comment_id>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('list/<slug:slug>/', CommentListView.as_view(), name='comment_list'),
    path('like/<int:comment_id>/', CommentLikeView.as_view(), name='comment-like'),
    path('dislike/<int:comment_id>/', CommentDislikeView.as_view(), name='comment-dislike'),
    path('unlike/<int:comment_id>/', CommentLikeDeleteView.as_view(), name='comment-unlike'),
]