from django.urls import path,include
from .import views
from .views import *


urlpatterns = [
    path('', views.inicio, name='inicio'),

    path('clientes', views.clientes, name='clientes'),
    path('clientes/crear', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar', views.editar_cliente, name='editar_cliente'),
    path('clientes/editar/<int:id>', views.editar_cliente, name='editar_cliente'),
    path('eliminar-cliente/<int:id>', views.eliminar_cliente, name='eliminar_cliente'),

    path('mesas', views.mesas, name='mesas'),
    path('mesas/crear', views.crear_mesa, name='crear_mesa'),
    path('mesas/editar', views.editar_mesa, name='editar_mesa'),
    path('mesas/editar/<int:id>', views.editar_mesa, name='editar_mesa'),
    path('eliminar-mesa/<int:id>', views.eliminar_mesa, name='eliminar_mesa'),

    path('reservacion', views.reservaciones, name='reservaciones'),
    path('reservacion/crear', views.crear_reservacion, name='crear_reservacion'),
    path('reservacion/editar/<int:id>', views.editar_reservacion, name='editar_reservacion'),
    path('eliminar-reservacion/<int:id>', views.eliminar_reservacion, name='eliminar_reservacion'),

    path('platos', views.platos, name='platos'),
    path('platos/crear', views.crear_plato, name='crear_plato'),
    path('platos/editar/<int:id>', views.editar_plato, name='editar_plato'),
    path('eliminar-platos/<int:id>', views.eliminar_plato, name='eliminar_plato'),

    path('menus/', views.lista_menus, name='menus'),  
    path('menus/crear/', views.crear_menu, name='crear_menu'),  
    path('menus/editar/<int:id>/', views.editar_menu, name='editar_menu'),  
    path('menus/eliminar/<int:id>/', views.eliminar_menu, name='eliminar_menu'),  
]