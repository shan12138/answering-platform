import Vue from 'vue'
import App from './App'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import router from './router/routers.js'
import axios from './axios/http.js'
import store from './vuex/store.js'
import Qs from 'qs'
import VideoData from './static_data/videoData'

Vue.config.productionTip = false
Vue.prototype.$axios = axios
Vue.prototype.$Qs = Qs
Vue.prototype.$videoData = VideoData
Vue.prototype.$successCode = '0000'
Vue.use(ElementUI)

new Vue({
  el: '#app',
  router,
  store,
  components: { App, },
  template: '<App/>',
})
