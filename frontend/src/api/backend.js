import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  withCredentials: true
})

// 登录接口
export const login = (username, password) => 
  api.post('/login', 
    { username, password },  // 确保字段名与后端一致
    {
      headers: {
        'Content-Type': 'application/json'  // 明确指定JSON格式
      }
    })

// 请求拦截器：自动添加token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api