from django.contrib import admin
from .models import Periodo, Asignatura, Profesor, Estudiante, Nota, DetalleNota

admin.site.register(Periodo)
admin.site.register(Asignatura)
admin.site.register(Profesor)
admin.site.register(Estudiante)
admin.site.register(Nota)
admin.site.register(DetalleNota)
