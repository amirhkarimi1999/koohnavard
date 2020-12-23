from django.urls import path

from . import views

app_name = 'planning'
urlpatterns = [
    path('', views.plans_list_view, name='all_plans_list'),
    path('club/<int:club_id>', views.plans_list_view, name='plans_list'),
    path('<int:plan_id>/', views.plan_profile_view, name='plan_view'),
    path('edit/<int:plan_id>', views.edit_plan_view, name='plan_edit'),
    path('<int:club_id>/new/', views.create_plan_view, name='plan_create'),
    path('preregister/<int:plan_id>/', views.plan_participant_preregister, name='plan_participant_preregister'),
    path('<int:plan_id>/members/', views.plan_members_and_requests_view, name='plan_join_members_and_requests'),
    path('admin/reqs/answer/<int:req_id>/<str:accept>/', views.answer_request_view, name='answer_plan_join_request'),
    path('<int:plan_id>/addduty/<int:req_id>/', views.addDuty, name='addDuty'),
]
