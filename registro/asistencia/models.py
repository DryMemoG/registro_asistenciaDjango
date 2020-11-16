from django.db import models

class Grado(models.Model):
    nombre= models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
class Actividad(models.Model):
    nombre=models.CharField(max_length=100)
    fecha=models.DateField()
    
    def __str__(self):
        return self.nombre
class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos= models.CharField(max_length=100)
    grado = models.ForeignKey(Grado, related_name="Grado", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre
        
class Asistencia(models.Model):
    nombre=models.CharField(max_length=100)
    alumno = models.ForeignKey(Estudiante, related_name="Estudiante", on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, related_name="Actividad", on_delete=models.CASCADE)
    reporte = models.CharField(max_length=2000)
    
    def __str__(self):
        return self.nombre