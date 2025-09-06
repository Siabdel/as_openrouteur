import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'

// Configuration d'Axios pour Django CSRF
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

// Configuration globale d'Axios
axios.defaults.baseURL = process.env.NODE_ENV === 'production' 
  ? window.location.origin 
  : 'http://localhost:8000'

// Configuration de Vue pour ignorer les warnings de production
Vue.config.productionTip = false

// Directive personnalisée pour le focus automatique
Vue.directive('focus', {
  inserted: function (el) {
    el.focus()
  }
})

// Filtre personnalisé pour formater les dates
Vue.filter('formatDate', function(value) {
  if (!value) return ''
  const date = new Date(value)
  return date.toLocaleString()
})

// Filtre pour tronquer le texte
Vue.filter('truncate', function(value, length) {
  if (!value) return ''
  if (value.length <= length) return value
  return value.substring(0, length) + '...'
})

// Installation des plugins globaux
Vue.prototype.$http = axios

// Initialisation de l'application Vue
new Vue({
  render: h => h(App),
  mounted() {
    // Initialiser AOS après le montage de l'application
    if (typeof AOS !== 'undefined') {
      AOS.init({
        duration: 800,
        once: true,
        offset: 10
      })
    }
    
    // Initialiser les tooltips Bootstrap
    if (typeof $ !== 'undefined') {
      $(document).ready(function() {
        $('[data-bs-toggle="tooltip"]').tooltip()
      })
    }
    
    // Gérer les événements avant de quitter la page
    window.addEventListener('beforeunload', this.handleBeforeUnload)
  },
  methods: {
    handleBeforeUnload(e) {
      if (Object.keys(this.$root.$data.chats || {}).length > 0) {
        e.preventDefault()
        e.returnValue = ''
        $('#leavePageModal').modal('show')
      }
    }
  },
  beforeDestroy() {
    window.removeEventListener('beforeunload', this.handleBeforeUnload)
  }
}).$mount('#app')

// Gestion des erreurs globales
Vue.config.errorHandler = function(err, vm, info) {
  console.error('Erreur Vue:', err, info)
  // Vous pourriez envoyer ces erreurs à un service de tracking ici
}

// Gestion des erreurs non capturées
window.addEventListener('error', function(e) {
  console.error('Erreur non capturée:', e.error)
})
