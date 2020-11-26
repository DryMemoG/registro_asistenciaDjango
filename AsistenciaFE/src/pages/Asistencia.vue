<template>
    <q-page class="flex flex-center">
        <div class="q-pa-md">
            <q-form
                class="q-gutter-md"
            >
            <q-input
                filled
                v-model="model0"
                label="Nombre de la Clase"
                hint="Clase o Fecha"
                lazy-rules
                :rules="[ val => val && val.length > 0 || 'Los campos deben llenarse']"
            />
            <q-select
                v-model="model"
                :options="actividadactual"
                label="Actividad"
            />
            <q-select
                v-model="model1"
                :options="alumnoactual"
                label="Alumno"
            />
            <q-input
                filled
                v-model="model2"
                label="Reporte"
                hint="Reporte"
                lazy-rules
                :rules="[ val => val && val.length > 0 || 'Los campos deben llenarse']"
            />
            <q-btn label="Guardar" @click="onSubmit" color="primary"/>
            </q-form>
        </div>
    </q-page>
</template>

<script>
export default {
    data() {
        return{
        model:null,
        model0:null,
        model1:null,
        model2:null,
            alumnos:[],
            actividades: [],
            alumnoactual:[],
            actividadactual:[],
        }
    },
    methods:{
        async onSubmit (){
            const query=`
                mutation createAsistencia($nombre: String!, $alumno: String!, $actividad: String!, $reporte: String!) {
                asistenciaCrear(nombre: $nombre, alumno: $alumno, actividad:$actividad, reporte: $reporte ){
                    asistencia{
                			id
                            }
                    }
            }
            `,
            
            variables= {
                nombre: this.model0,
                alumno: (this.model1).split(';',1).toString(),
                actividad: (this.model).split(';',1).toString(),
                reporte: this.model2
            }
            console.log(query, variables)
            const data = await this.$graphql(query,variables);
            if(data.message = "OK" && data.data){
                if(data.data.asistenciaCrear){
                    console.log("Exito")
                    location.reload();
                }
                else{
                    console.log("error")
                }
                    
            }
            else{
                console.log("Error")
            }
        }
    },
    async created(){
        const query= `
        query {
            allEstudiantes{
                edges{
                    node{ 
                        nombre, apellidos
                    }
                }
            }
        }`,
        data = await this.$graphql(query,{});
        if(data.data.allEstudiantes){
            var arraytemp=[];
            data.data.allEstudiantes.edges.forEach(estudiante => {
                arraytemp.push(estudiante);
            });
            this.alumnos.push(arraytemp)
        }
        var contador = 0;
        this.alumnos.forEach(alumno => {
            alumno.forEach(elemento =>{
            
                this.alumnoactual.push(
                    contador + ';' +elemento.node.nombre + ' ' + elemento.node.apellidos
                
                )
                contador++;
            }
        )
        console.log(this.alumnoactual)
        
    })
    const query2= `
        query {
            allActividades{
                edges{
                    node{ 
                        nombre, fecha
                    }
                }
            }
        }`,
        data2 = await this.$graphql(query2,{});
        if(data2.data.allActividades){
            var arraytemp2=[];
            data2.data.allActividades.edges.forEach(actividad => {
                arraytemp2.push(actividad);
            });
            this.actividades.push(arraytemp2)
            
        }
        var contador=0
        this.actividades.forEach(actividad => {
            actividad.forEach(elemento =>{
                this.actividadactual.push(
                contador+';'+ elemento.node.nombre + ' ' + elemento.node.fecha
                
                )
                contador++;
            }
        )
        console.log(this.actividadactual)
        
    })
    
    }   
}
</script>