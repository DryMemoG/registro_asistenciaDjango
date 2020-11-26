import Vue from 'vue'
import axios from 'axios'

Vue.prototype.$axios = axios

const graphql = require('graphql-client')({
    url: "http://localhost:8000/graphql"
})

Vue.prototype.$graphql =
    (query, variables) => graphql.query(query, variables).then(response => {
        //console.log(response)
        return {
            'message': 'OK',
            'data': response.data
        }
    }).catch(e => {
        console.log(e)
        return {
            'message': 'ERROR',
            'error': e
        }
    }) 