<template>
  <div class="login">
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <input v-model="form.username" placeholder="Username" required>
      <input v-model="form.password" type="password" placeholder="Password" required>
      <button type="submit">Login</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const form = ref({ username: 'admin', password: 'secret' })
const error = ref(null)

const handleLogin = async () => {
  try {
    const success = await authStore.login(form.value.username, form.value.password)
    if (success) {
      router.push('/')
    } else {
      error.value = 'Login failed'
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Unknown error'
  }
}
</script>