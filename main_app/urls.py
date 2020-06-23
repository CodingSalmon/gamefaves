from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('games/<int:game_id>/', views.games_detail, name='detail'),
    path('games/create/', views.GameCreate.as_view(), name='games_create'),
    path('games/<int:pk>/delete', views.GameDelete.as_view(), name='games_delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/<int:user_id>/', views.user_detail, name='user_detail'),
    path('games/<int:game_id>/assoc_favgame/<int:user_id>/', views.assoc_favgame, name='assoc_favgame'),
    path('games/<int:game_id>/unassoc_favgame/<int:user_id>/', views.unassoc_favgame, name='unassoc_favgame'),
]
