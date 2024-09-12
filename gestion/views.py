from django.shortcuts import render, redirect
from .models import *
from .forms import *
from datetime import datetime,timedelta
from django.contrib import messages
from django.utils import timezone


# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')


#clientes#######################################################################
def clientes(request):
    clientes= Cliente.objects.all()
    return render(request, 'tablas/listar_cliente.html', {'clientes' : clientes })

def crear_cliente(request):
    formulario= Clienteform(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('clientes')
    return render(request, 'plantillas/crear_todo.html', {'formulario': formulario})

def editar_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    formulario = Clienteform(request.POST or None, request.FILES or None, instance=cliente)
    if formulario.is_valid() and request.method == 'POST':
        formulario.save()
        return redirect('clientes')
    return render(request, 'plantillas/editar_todo.html', {'formulario': formulario})

def eliminar_cliente(request, id):
    something = Cliente.objects.get(id=id)
    something.delete()
    return redirect('clientes')

#mesa#######################################################################

def mesas(request):
    mesas= Mesa.objects.all()
    return render(request, 'tablas/listar_mesa.html', {'mesas' : mesas })

def crear_mesa(request):
    formulario= Mesaform(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('mesas')
    return render(request, 'plantillas/crear_todo.html', {'formulario': formulario})

def editar_mesa(request, id):
    mesa = Mesa.objects.get(id=id)
    formulario = Mesaform(request.POST or None, request.FILES or None, instance=mesa)
    if formulario.is_valid() and request.method == 'POST':
        formulario.save()
        return redirect('mesas')
    return render(request, 'plantillas/editar_todo.html', {'formulario': formulario})

def eliminar_mesa(request, id):
    something = Mesa.objects.get(id=id)
    something.delete()
    return redirect('mesas')

#reservacion#######################################################################

def reservaciones(request):
    reservacion= Reservacion.objects.all()
    return render(request, 'tablas/listar_reservacion.html', {'reservacion' : reservacion })


def editar_reservacion(request, id):
    reservacion = Reservacion.objects.get(id=id)
    formulario = Reservacionform(request.POST or None, request.FILES or None, instance=reservacion)
    if formulario.is_valid() and request.method == 'POST':
        formulario.save()
        return redirect('reservaciones')
    return render(request, 'plantillas/editar_todo.html', {'formulario': formulario})

def eliminar_reservacion(request, id):
    something = Reservacion.objects.get(id=id)
    something.delete()
    return redirect('reservaciones')


#platos#######################################################################

def platos(request):
    platos= Plato.objects.all()
    return render(request, 'tablas/listar_platos.html', {'platos' : platos })

def crear_plato(request):
    formulario= Platoform(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('platos')
    return render(request, 'plantillas/crear_todo.html', {'formulario': formulario})

def editar_plato(request, id):
    plato = Plato.objects.get(id=id)
    formulario = Reservacionform(request.POST or None, request.FILES or None, instance=plato)
    if formulario.is_valid() and request.method == 'POST':
        formulario.save()
        return redirect('plato')
    return render(request, 'plantillas/editar_todo.html', {'formulario': formulario})

def eliminar_plato(request, id):
    something = Plato.objects.get(id=id)
    something.delete()
    return redirect('platos')

#menu#######################################################################

def menus(request):
    menu= Menu.objects.all()
    return render(request, 'tablas/listar_menu.html', {'menu' : menu })

def crear_menu(request):
    formulario= Menuform(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('menus')
    return render(request, 'plantillas/crear_todo.html', {'formulario': formulario})

def editar_menu(request, id):
    menu= Menu.objects.get(id=id)
    formulario = Reservacionform(request.POST or None, request.FILES or None, instance=menu)
    if formulario.is_valid() and request.method == 'POST':

        formulario.save()
        return redirect('menus')
    return render(request, 'plantillas/editar_todo.html', {'formulario': formulario})

def eliminar_menu(request, id):
    something = Menu.objects.get(id=id)
    something.delete()
    return redirect('menus')



def lista_menus(request):
    fecha_consulta = request.GET.get('fecha')
    menus = Menu.objects.all().prefetch_related('platos')

    if fecha_consulta:
        try:
            fecha = datetime.strptime(fecha_consulta, '%d/%m/%Y').date()
        except ValueError:
            try:
                fecha = datetime.strptime(fecha_consulta, '%Y-%m-%d').date()
            except ValueError:
                error_mensaje = "Formato de fecha inválido. Use DD/MM/YYYY o YYYY-MM-DD."
                fecha = None

        if fecha:
            menus = menus.filter(fecha_disponible=fecha)

    context = {
        'menus': menus,
        'fecha_consulta': fecha_consulta,
        'error_mensaje': error_mensaje if 'error_mensaje' in locals() else None,
        'debug_info': {
            'total_menus': menus.count(),
            'fecha_consulta': fecha_consulta,
            'menus_list': [f"{menu.id}: {menu.nombre} ({menu.fecha_disponible})" for menu in menus]
        }
    }
    return render(request, 'tablas/listar_menu.html', context)


def verificar_disponibilidad_mesa(mesa, fecha_orden, duracion):
    if timezone.is_naive(fecha_orden):
        fecha_orden = timezone.make_aware(fecha_orden)
    
    fecha_fin = fecha_orden + duracion

    reservaciones_existentes = Reservacion.objects.filter(
        mesa=mesa,
        estado__in=['pendiente', 'confirmada']
    )
    
    for reservacion in reservaciones_existentes:
        reserva_inicio = reservacion.fecha_orden
        reserva_fin = reserva_inicio + reservacion.duracion

        if (fecha_orden < reserva_fin) and (fecha_fin > reserva_inicio):
            return False

    return True


def crear_reservacion(request):
    if request.method == 'POST':
        formulario = Reservacionform(request.POST)
        if formulario.is_valid():
            mesa = formulario.cleaned_data['mesa']
            fecha_orden = formulario.cleaned_data['fecha_orden']
            duracion = formulario.cleaned_data['duracion']
            if isinstance(duracion, timedelta):
                duracion_timedelta = duracion
            else:
                horas, minutos = map(int, duracion.split(':'))
                duracion_timedelta = timedelta(hours=horas, minutes=minutos)

            if verificar_disponibilidad_mesa(mesa, fecha_orden, duracion_timedelta):
                nueva_reservacion = formulario.save(commit=False)
                nueva_reservacion.estado = 'pendiente'
                nueva_reservacion.save()
                messages.success(request, "Reservación creada exitosamente.")
                return redirect('reservaciones')
            else:
                messages.error(request, "La mesa ya está reservada para la fecha y hora seleccionadas.")
                return render(request, 'plantillas/crear_todo.html', {'formulario': formulario})
    else:
        formulario = Reservacionform()
    
    return render(request, 'plantillas/crear_todo.html', {'formulario': formulario})