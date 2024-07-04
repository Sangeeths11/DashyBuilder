export default defineNuxtRouteMiddleware((to, from) => {
    const user = useSupabaseUser()
    if (!user.value && to.path !== '/login' && to.path !== '/register') {
      return navigateTo('/login')
    }
})