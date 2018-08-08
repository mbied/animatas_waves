import Vue from 'vue'
import Vddl from 'vddl'
import App from './App'
import router from './router'

Vue.use(Vddl)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
