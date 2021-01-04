from django.urls import path

from . import views

app_name = 'participation'
urlpatterns = [
    path('', views.clubs_list_view, name='clubs_list'),
    path('<int:club_id>/', views.club_profile_view, name='club_view'),
    path('<int:club_id>/edit/', views.edit_club_view, name='club_edit'),
    path('<int:club_id>/requests/', views.club_requests_view, name='club_join_requests'),
    path('new/', views.create_club_view, name='club_create'),
    path('<int:club_id>/join/', views.join_request_view, name='club_join'),
    path('<int:club_id>/leave/', views.leave_request_view, name='club_leave'),
    path('admin/reqs/answer/<int:req_id>/<int:accept>/', views.answer_request_view, name='answer_club_join_request'),
    path('admin/members/kick/<int:req_id>/', views.kick_club_member_view, name='kick_club_member'),
]

