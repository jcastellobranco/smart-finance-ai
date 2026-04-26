<script setup lang="ts">
onMounted(() => {
  const auth = useAuthStore()
  auth.hydrate()
  navigateTo(auth.isAuthenticated ? '/dashboard' : '/login')
})
</script>

<template>
  <main class="app-page">
    <div class="app-shell">
      <ProgressSpinner />
    </div>
  </main>
</template>
