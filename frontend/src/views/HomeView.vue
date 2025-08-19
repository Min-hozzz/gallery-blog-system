<template>
  <div>
    <h1>Welcome</h1>
    <p v-if="authStore.token">Logged in</p>
    <p v-else>Not logged in</p>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
const authStore = useAuthStore()
</script>