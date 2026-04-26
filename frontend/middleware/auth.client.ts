export default defineNuxtRouteMiddleware(async () => {
  const auth = useAuthStore()
  auth.hydrate()

  if (!auth.isAuthenticated) {
    return navigateTo('/login')
  }

  if (!auth.user) {
    try {
      await auth.fetchMe()
    } catch {
      auth.clear()
      return navigateTo('/login')
    }
  }
})
