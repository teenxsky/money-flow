<template>
  <div class="flex min-h-screen items-center justify-center bg-gray-50">
    <div class="card">
      <div class="card-body">
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div>
            <h2 class="text-2xl font-bold text-gray-900 text-center">Sign In</h2>
            <p class="mt-2 text-sm text-gray-600 text-center">
              Enter your credentials to access your account
            </p>
          </div>

          <div
            v-if="errorMessage && errorMessage.error"
            class="bg-red-50 border border-red-200 rounded-md p-4"
          >
            <div class="flex">
              <div class="flex-shrink-0">
                <ExclamationTriangleIcon class="h-5 w-5 text-red-400" />
              </div>
              <div class="ml-3">
                <div class="text-sm text-red-800">
                  {{ errorMessage.message }}
                  <ul class="mt-1 list-disc pl-5">
                    <li>
                      {{ errorMessage.error }}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <div class="space-y-4">
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                autocomplete="email"
                required
                class="input-field"
                placeholder="your@email.com"
              />
            </div>

            <div>
              <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
              <input
                id="password"
                v-model="form.password"
                type="password"
                autocomplete="current-password"
                required
                class="input-field"
                placeholder="Enter your password"
              />
            </div>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span
              v-if="loading"
              class="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"
            ></span>
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>

          <div class="text-center">
            <p class="text-sm text-gray-600">
              Don't have an account?
              <NuxtLink
                to="/auth/register"
                class="font-medium text-primary-600 hover:text-primary-500"
              >
                Sign up
              </NuxtLink>
            </p>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline'

  definePageMeta({
    layout: 'auth'
  })

  const authStore = useAuthStore()

  const loading = ref(false)

  const form = ref({
    email: '',
    password: ''
  })

  const errorMessage = computed(() => {
    if (!authStore.loginResult) return ''

    const { message, error } = authStore.loginResult
    return { message, error }
  })

  const handleLogin = async () => {
    loading.value = true

    try {
      const result = await authStore.login(form.value.email, form.value.password)

      if (result.success) {
        await navigateTo('/dashboard')
      }
    } catch (err) {
      console.error('Login error:', err)
    } finally {
      loading.value = false
    }
  }
</script>
