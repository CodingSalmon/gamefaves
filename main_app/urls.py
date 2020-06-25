from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('games/<int:game_id>/', views.games_detail, name='detail'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/<int:user_id>/', views.user_detail, name='user_detail'),
    path('games/create/', views.GameCreate.as_view(), name='games_create'),
    path('games/<int:game_id>/delete/', views.game_delete, name='game_delete'),
    path('games/<int:game_id>/add_review/', views.add_review, name='add_review'),
    path('games/<int:game_id>/delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('games/<int:game_id>/assoc_favgame/<int:user_id>/', views.assoc_favgame, name='assoc_favgame'),
    path('games/<int:game_id>/unassoc_favgame/<int:user_id>/', views.unassoc_favgame, name='unassoc_favgame'),
    path('games/<int:game_id>/add_photo/', views.add_photo, name='add_photo'),
    path('games/<int:game_id>/delete_photo/', views.delete_photo, name='delete_photo'),
]
