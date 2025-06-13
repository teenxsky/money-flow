export default defineNuxtRouteMiddleware(to => {
  const authStore = useAuthStore()

  if (process.server) return

  authStore.initializeAuth()

  if (!authStore.isAuthenticated && !to.path.startsWith('/auth')) {
    return navigateTo('/auth/login')
  }

  if (authStore.isAuthenticated && to.path.startsWith('/auth')) {
    return navigateTo('/dashboard')
  }
})
