from django.contrib import admin
from asistencia.models import Grado, Actividad, Estudiante,Asistencia

# Register your models here.
admin.site.register(Grado)
admin.site.register(Actividad)
admin.site.register(Estudiante)
admin.site.register(Asistencia)
