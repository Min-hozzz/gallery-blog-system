<script setup>
import { ref } from 'vue'
import api from '@/api/backend'
import { useRouter } from 'vue-router'

const form = ref({ username: '', password: '' })
const router = useRouter()

const handleLogin = async () => {
  try {
    const res = await api.post('/login', form.value)
    localStorage.setItem('access_token', res.data.access_token)
    router.push('/blog')
  } catch (err) {
    alert('登录失败')
  }
}
</script>

<template>
  <form @submit.prevent="handleLogin">
    <input v-model="form.username" placeholder="用户名">
    <input v-model="form.password" type="password" placeholder="密码">
    <button type="submit">登录</button>
  </form>
</template>