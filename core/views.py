from django.shortcuts import render
from .models import Periodo, Asignatura, Profesor, Estudiante, Nota, DetalleNota

def home(request):
    return render(request, 'base.html')

def periodo_list(request):
    periodos = Periodo.objects.all()
    return render(request, 'periodo_list.html', {'periodos': periodos})

def asignatura_list(request):
    asignaturas = Asignatura.objects.all()
    return render(request, 'asignatura_list.html', {'asignaturas': asignaturas})

def profesor_list(request):
    profesores = Profesor.objects.all()
    return render(request, 'profesor_list.html', {'profesores': profesores})

def estudiante_list(request):
    estudiantes = Estudiante.objects.all()
    return render(request, 'estudiante_list.html', {'estudiantes': estudiantes})

def nota_list(request):
    notas = Nota.objects.all()
    return render(request, 'nota_list.html', {'notas': notas})

def detallenota_list(request):
    detallenotas = DetalleNota.objects.all()
    return render(request, 'detallenota_list.html', {'detallenotas': detallenotas})
