from django.db import models
from django.utils import timezone

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(state=True)

class BaseModel(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    state = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()

    def delete(self, *args, **kwargs):
        self.state = False
        self.save()

    class Meta:
        abstract = True

class Periodo(BaseModel):
    periodo = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Periodo Lectivo " + self.periodo

class Asignatura(BaseModel):
    descripcion = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.descripcion

class Profesor(BaseModel):
    nombre = models.CharField(max_length=50)
    dni = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Profesor " + self.nombre

class Estudiante(BaseModel):
    nombre = models.CharField(max_length=50)
    dni = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Nota(BaseModel):
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notas de {self.asignatura.descripcion} - Periodo Lectivo {self.periodo.periodo} - Profesor {self.profesor.nombre}"
    
class DetalleNota(BaseModel):
    nota = models.ForeignKey(Nota, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    nota1 = models.FloatField(null=True, blank=True)
    nota2 = models.FloatField(null=True, blank=True)
    recuperacion = models.FloatField(null=True, blank=True)
    observacion = models.CharField(max_length=200, blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Detalles {self.nota}"

    class Meta:
        unique_together = ('nota', 'estudiante')

