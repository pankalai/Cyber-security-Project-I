from django.urls import path

from .views import index, register, login, logout, admin, get, add, csrf

urlpatterns = [
    path('', index, name='index'),
    path('register', register, name='register'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('admin', admin, name='admin'),
    path('get', get, name='get'),
    path('add', add, name='add'),
    path('csrf', csrf, name='csrf')
]