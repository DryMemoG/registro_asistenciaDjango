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
        interfaces = (relay.Node,)
        
class EstudianteNode(DjangoObjectType):
    class Meta:
        model = Estudiante
        filter_fields = {'nombre':['exact', 'icontains','istartswith'],
        'apellidos': ['exact','icontains','istartswith'],
        'grado':['exact'],
        }
        interfaces = (relay.Node,)

class AsistenciaNode(DjangoObjectType):
    class Meta:
        model = Asistencia
        filter_fields = {'nombre' :['exact','icontains', 'istartswith'],
        'alumno':['exact'],
        'actividad':['exact'],
        'reporte':['icontains'],
        }
        interfaces = (relay.Node,)

class Query(graphene.ObjectType):
    grado = relay.Node.Field(GradoNode)
    all_grados = DjangoFilterConnectionField(GradoNode)
    
    actividad = relay.Node.Field(ActividadNode)
    all_actividades = DjangoFilterConnectionField(ActividadNode)
    
    estudiante = relay.Node.Field(EstudianteNode)
    all_estudiantes = DjangoFilterConnectionField(EstudianteNode)
    
    asistencia = relay.Node.Field(AsistenciaNode)
    all_asistencias = DjangoFilterConnectionField(AsistenciaNode)

class ActividadModel(DjangoObjectType):
    class Meta:
        model = Actividad
        
class ActividadCrear(graphene.Mutation):
    actividad = graphene.Field(ActividadModel)
    
    class Arguments:
        nombre= graphene.String(required=True)
        fecha = graphene.Date(required=True)
    
    def mutate(self, info, nombre, fecha):
        actividad = Actividad(nombre = nombre, fecha= fecha)
        actividad.save()
        return ActividadCrear(actividad=actividad)

class AsistenciaModel(DjangoObjectType):
    class Meta:
        model = Asistencia
        
class AsistenciaCrear(graphene.Mutation):
    asistencia = graphene.Field(AsistenciaModel)
    
    class Arguments:
        nombre = graphene.String(required=True)
        alumno = graphene.String(required=True)
        actividad = graphene.String(required=True)
        reporte = graphene.String(required=True)
        
    def mutate(self, info, nombre,alumno,actividad,reporte):
        alumno = Estudiante.objects.get(Estudiante=alumno)
        actividad = Actividad.objects.get(Actividad=actividad)
        asistencia = Asistencia(nombre=nombre,alumno=alumno,actividad=actividad,reporte=reporte)
        asistencia.save()
        return AsistenciaCrear(asistencia=asistencia)

class Mutation(graphene.ObjectType):
    actividad_crear = ActividadCrear.Field()
    asistencia_crear = AsistenciaCrear.Field()
    
