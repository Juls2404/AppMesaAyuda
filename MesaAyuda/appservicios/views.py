from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from appservicios.models import *
from random import *
from django.db import Error, transaction
from datetime import datetime
 # Para el correo
 
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import threading
from smtplib import SMTPException 

# Create your views here.
def inicio(request):
    return render (request, "formulario.html")

# En esta parte estamos definiendo los inicios de los roles 

def inicioAdministrador (request):
    if request.user.is_authenticated:
        datosSesion = {"user": request.user,
                        "rol": request.user.groups.get().name}
        
        return render (request, "admin/inicio.html", datosSesion)
    else:
        mensaje = "Debe iniciar sesión"
        return render (request, "formulario.html", {"mensaje": mensaje})


def inicioTecnico(request):
    if request.user.is_authenticated:
        datosSesion = {"user": request.user,
                        "rol": request.user.groups.get().name}
        return render(request, "tecnico/inicio.html", datosSesion)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request, "formulario.html", {"mensaje":mensaje})

def inicioEmpleado(request):
    if request.user.is_authenticated:
        datosSesion = {"user": request.user,
                        "rol": request.user.groups.get().name}
        return render(request, "empleado/inicio.html", datosSesion)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request, "formulario.html", {"mensaje":mensaje})

def login (request):
    username = request.POST ["User"]
    password = request.POST ["Password"]
    user = authenticate(username = username, password = password)
    
    if user is not None:
    #Aquí se registra la variable de sesión 
        auth.login(request,user)
        if user.groups.filter(name = 'administrador'). exists():
            return redirect ('/inicioAdministrador')
    
        elif user.groups.filter(name='Tecnico'). exists():
            return redirect ('/inicioTecnico')
    
        else: return redirect ('/inicioEmpleado')
    else:
        mensaje = "Tu usuario o contraseña son incorrectos"
        return render (request, "formulario.html",{"mensaje": mensaje})
    

def vistaSolicitud(request):
    if request.user.is_authenticated:
        oficinaAmbientes = OficinaAmbiente.objects.all()
        datosSesion = { "user": request.user,
                        "rol": request.user.groups.get().name,
                        'oficinaAmbiente': oficinaAmbientes}
        mensaje = "Debe iniciar sesión"
        return render(request, 'empleado/solicitud.html',{"mensaje": mensaje})

def registroSolicitud(request):
    
    try:
        with transaction.atomic():
            user = request.user
            descripcion = request.POST ['descripción']
            idOfAmb = request. POST ['idOfAmb']
            oficinaAmbiente = OficinaAmbiente.objects.get(pk=idOfAmb)
            solicitud = Solicitud (solUsuario = user,
                                    solDescripción = descripcion,
                                    solOficinaAmbiente = oficinaAmbiente)
            solicitud.save()
            consecutivoCaso= randint(1,10000)
            codigoCaso = "REQ" + str (consecutivoCaso). rjust (5,'0')
            userCaso = user.objects.filter(groups__name__in=['Administrador'])
            estado = "Solicitada"
            caso = Caso (casSolicitud = solicitud,
                            casCodigo = codigoCaso,
                            casUsuario = userCaso,
                            casEstado =  estado
                            )
            caso.save
    except Error as error:
        transaction.rollback()
        mensaje = f"{error}"
        
        


def salir(request):
    auth.logout(request)
    return render(request, "formulario.html", {"mensaje": "Ha cerrado la sesión"})