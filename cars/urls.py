from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('cars/', views.car_list, name='car_list'),

    path('cars/<int:pk>/', views.car_detail, name='car_detail'),

    path('cars/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),

    path('favorites/', views.favorites, name='favorites'),

    path('cars/<int:pk>/compare/', views.add_compare, name='add_compare'),

    path('compare/remove/<int:pk>/', views.remove_compare, name='remove_compare'),

    path('compare/', views.compare, name='compare'),

    # AUTH
    path('login/', views.user_login, name='user_login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='user_logout'),

    # TEST DRIVE
    path('cars/<int:pk>/test-drive/', views.test_drive, name='test_drive'),
    path(
        'cars/<int:pk>/order/',
        views.create_order,
        name='create_order'
    ),
    path('about/', views.about, name='about'),
]
