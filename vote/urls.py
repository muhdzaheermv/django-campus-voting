from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from vote import views

urlpatterns = [
    path('', views.index, name='index'),  # Root URL shows the index page
    path("register_manager/", views.register_manager, name="register_manager"),
    path("login_manager/", views.login_manager, name="login_manager"),
    path("manager/<int:manager_id>/dashboard/", views.manager_dashboard, name="manager_dashboard"),

    path("manager/<int:manager_id>/campaigns/create/", views.create_campaign, name="create_campaign"),
    path("manager/<int:manager_id>/campaigns/", views.campaign_list, name="campaign_list"),  # ✅ Correct pattern
    path("campaigns/edit/<int:campaign_id>/", views.edit_campaign, name="edit_campaign"),
    path("campaigns/delete/<int:campaign_id>/", views.delete_campaign, name="delete_campaign"),  # ✅ Delete campaign
    path("campaigns/<int:campaign_id>/elections/create/", views.create_election, name="create_election"),  # ✅ Create election

    

    
    path("elections/edit/<int:election_id>/", views.edit_election, name="edit_election"),
    path("elections/delete/<int:election_id>/", views.delete_election, name="delete_election"),  # ✅ Delete election

    path("manager/<int:manager_id>/profile/", views.view_profile, name="view_profile"),
    path("elections/edit/<int:election_id>/", views.edit_election, name="edit_election"),  # ✅ Edit election

    path("elections/<int:election_id>/candidates/create/", views.create_candidate, name="create_candidate"),
    path("candidates/<int:candidate_id>/delete/", views.delete_candidate, name="delete_candidate"),
    path("candidates/<int:candidate_id>/edit/", views.edit_candidate, name="edit_candidate"),

    path("campaigns/<int:campaign_id>/voters/upload/", views.upload_voters, name="upload_voters"),
    path("campaigns/<int:campaign_id>/voters/", views.voters_list, name="voters_list"),

    path("campaigns/<int:campaign_id>/voters/delete_all/", views.delete_all_voters, name="delete_all_voters"),

    path("voter/login/", views.voter_login, name="voter_login"),
    path("voter/dashboard/<int:voter_id>/", views.voter_dashboard, name="voter_dashboard"),

    path("voter/<int:voter_id>/dashboard/", views.voter_dashboard, name="voter_dashboard"),
    path("voter/<int:voter_id>/vote/", views.vote_page, name="vote_page"),
    path("elections/<int:election_id>/vote/submit/", views.submit_vote, name="submit_vote"),

    path('campaigns/<int:campaign_id>/voters/approve/', views.approve_voters, name='approve_voters'),
    path('voter/<int:voter_id>/approve/', views.approve_voter, name='approve_voter'),
    path('voter/<int:voter_id>/disapprove/', views.disapprove_voter, name='disapprove_voter'),

    path("elections/<int:election_id>/results/", views.election_results, name="election_results"),

    path('officer/register/', views.register_election_officer, name='register_election_officer'),

     path('officer/login/', views.election_officer_login, name='election_officer_login'),
    path("officer/<int:officer_id>/dashboard/", views.officer_dashboard, name="officer_dashboard"),

    path("officer/<int:officer_id>/dashboard/", views.officer_dashboard, name="officer_dashboard"),
    path("campaigns/<int:campaign_id>/voters/upload/", views.upload_voters, name="upload_voters"),
    path("campaigns/<int:campaign_id>/candidates/manage/", views.manage_candidates, name="manage_candidates"),

    
    path("campaigns/<int:campaign_id>/candidates/add/", views.add_candidate, name="add_candidate"),
    path("candidates/<int:candidate_id>/edit/", views.edit_candidate, name="edit_candidate"),
    path("candidates/<int:candidate_id>/delete/", views.delete_candidate, name="delete_candidate"),

    path("manager/<int:manager_id>/register_presiding_officer/", views.register_presiding_officer, name="register_presiding_officer"),
    path("manager/<int:manager_id>/register_presiding_officer_officer/", views.register_presiding_officer_officer, name="register_presiding_officer_officer"),
    path("presiding_officer/login/", views.presiding_officer_login, name="presiding_officer_login"),
    path("presiding_officer/<int:officer_id>/dashboard/", views.presiding_officer_dashboard, name="presiding_officer_dashboard"),

    path('logout/', views.logout_view, name='logout'),


    path('manager/<int:manager_id>/profile/edit/', views.manager_profile, name='manager_profile'),
    


    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
