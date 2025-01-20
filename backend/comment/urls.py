from django.urls import path
from comment.views import (
    CommentRegisterView,
    CommentEditView,
    CommentDeleteView,
    CommentListView,
    LikeView,
    DislikeView,
    LikeDeleteView,
    ReportRegisterView,
    ReportEditView,
    ReportDeleteView,
    ReportListView,
    PoolRegisterView,
    PoolEditView,
    PoolDeleteView,
    PoolListView,
    VoteOptionView,
    UnvoteOptionView
)

urlpatterns = [
    path('register/',CommentRegisterView.as_view(), name='comment_register'),
    path('edit/<int:comment_id>/',CommentEditView.as_view(), name='comment_edit'),
    path('delete/<int:comment_id>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('list/<slug:slug>/', CommentListView.as_view(), name='comment_list'),
    path('like/<int:comment_id>/', LikeView.as_view(), name='like'),
    path('dislike/<int:comment_id>/', DislikeView.as_view(), name='dislike'),
    path('unlike/<int:comment_id>/', LikeDeleteView.as_view(), name='unlike'),
    path('report/register/',ReportRegisterView.as_view(), name='report_register'),
    path('report/edit/<int:report_id>/',ReportEditView.as_view(), name='report_edit'),
    path('report/delete/<int:report_id>/',ReportDeleteView.as_view(), name='report_edit'),
    path('report/list/<slug:slug>/', ReportListView.as_view(), name='report_list'),

    path('pool/register/',PoolRegisterView.as_view(), name='pool_register'),
    path('pool/edit/<int:pool_id>/',PoolEditView.as_view(), name='pool_edit'),
    path('pool/delete/<int:pool_id>/',PoolDeleteView.as_view(), name='pool_edit'),
    path('pool/list/<slug:slug>/', PoolListView.as_view(), name='pool_list'),

    path('vote/<int:option_id>/', VoteOptionView.as_view(), name='vote'),
    path('unvote/<int:option_id>/', UnvoteOptionView.as_view(), name='unvote'),
]