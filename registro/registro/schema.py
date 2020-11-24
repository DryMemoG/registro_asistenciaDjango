import graphene
import asistencia.schema

class Query(asistencia.schema.Query, graphene.ObjectType):
    pass
    
schema = graphene.Schema(query=Query)
