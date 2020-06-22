from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('games/<int:game_id>/', views.games_detail, name='detail'),
    path('games/create/', views.GameCreate.as_view(), name='games_create'),
    path('games/<int:pk>/delete', views.GameDelete.as_view(), name='games_delete'),
    path('accounts/signup/', views.signup, name='signup'),
]
