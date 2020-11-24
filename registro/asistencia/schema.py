import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from asistencia.models import Grado, Actividad, Estudiante, Asistencia

class GradoNode(DjangoObjectType):
    class Meta:
        model = Grado
        filter_fields = ['nombre']
        interfaces = (relay.Node,)
        
class ActividadNode(DjangoObjectType):
    class Meta:
        model = Actividad
        filter_fields = {'nombre':['exact','icontains', 'istartswith'],
        'fecha':['exact'],}
        interfaces = (relay.Node)
        
class EstudianteNode(DjangoObjectType):
    class Meta:
        model = Estudiante
        filter_fields = {'nombre':['exact', 'icontains','istartswith'],
        'apellidos': ['exact','icontains','istartswith'],
        'grado':['exact'],
        }
        interfaces = (relay.Node)

class AsistenciaNode(DjangoObjectType):
    class Meta:
        model = Asistencia
        filter_fields = {'nombre' :['exact','icontains', 'istartswith'],
        'alumno':['exact','icontains', 'istartswith'],
        'actividad':['exact','icontains', 'istartswith'],
        'reporte':['icontains'],
        }
        interfaces = (relay.Node)

class Query(graphene.ObjectType):
    grado = relay.Node.Field(GradoNode)
    all_grados = DjangoFilterConnectionField(GradoNode)
    
    actividad = relay.Node.Field(ActividadNode)
    all_actividades = DjangoFilterConnectionField(ActividadNode)
    
    estudiante = relay.Node.Field(EstudianteNode)
    all_estudiantes = DjangoFilterConnectionField(EstudianteNode)
    
    asistencia = relay.Node.Field(AsistenciaNode)
    all_asistencias = DjangoFilterConnectionField(AsistenciaNode)
