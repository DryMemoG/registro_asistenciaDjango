<template>
  <q-page class="flex flex-center">
    <div class="q-pa-md">
    <q-table
      title="Registro de Asistencia"
      :data="data"
      :columns="columns"
      row-key="name"
      dark
      color="amber"
    />
  </div>
  </q-page>
</template>

<script>
export default {
  name: 'PageIndex',
  data () {
    return {
    temp: [],
    asistenciainfo:{
      actividad:{
        fecha: new Date(),
        nombre: null,
      },
      alumno: {
        nombre: null,
        apellidos:null
      },
      nombre: null,
      reporte: null
    },
      all_asistencias: [],
      asistencias: [],
      columns: [
        { name: 'nombre', label: 'Actividad', field: 'nombre' },
        { name: 'actividad', label: 'Evento', field: 'actividad' },
        { name: 'alumno', label: 'Alumno', field: 'alumno' },
        { name: 'reporte', label: 'Reporte', field: 'reporte' }
      ],
      data: [],
    }
  },
  methods: {
  fill(){
    
      
  }
  }, 
    async created() {
      const query = `  
        query {
          allAsistencias{
            edges{
              node{
              id,
                nombre, actividad {
                  nombre,fecha
                }, alumno {
                  nombre,apellidos
                }, reporte
              }
            }
          }
        }`
      const data = await this.$graphql(query, {})
      if (data.data.allAsistencias){
        var arraytemp = [];
        data.data.allAsistencias.edges.forEach(asistencia => {
          arraytemp.push(asistencia);
          
        });
        this.asistencias.push(arraytemp);
        
      }
      this.all_asistencias=this.asistencias
      this.all_asistencias.forEach(asistencia => {
          asistencia.forEach(elemento =>{
          this.data.push({
            nombre: elemento.node.nombre,
            actividad: (elemento.node.actividad.nombre + ' ' +elemento.node.actividad.fecha),
            alumno: (elemento.node.alumno.nombre +' '+ elemento.node.alumno.apellidos),
            reporte: (elemento.node.reporte)}
          )
          } )
        })
      
    }
}
</script>
