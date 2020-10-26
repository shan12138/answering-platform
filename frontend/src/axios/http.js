import axios from 'axios'
const token = sessionStorage.getItem('token')
axios.defaults.withCredentials = true
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
axios.defaults.headers.common.Authorization = 'JWT ' + token
axios.defaults.baseURL = '/api'
export default axios
