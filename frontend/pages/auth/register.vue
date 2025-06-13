<template>
  <div class="flex min-h-screen items-center justify-center bg-gray-50">
    <div class="card">
      <div class="card-body">
        <form @submit.prevent="handleRegister" class="space-y-6">
          <div>
            <h2 class="text-2xl font-bold text-gray-900 text-center">Create Account</h2>
            <p class="mt-2 text-sm text-gray-600 text-center">
              Sign up to start managing your finances
            </p>
          </div>

          <div
            v-if="errorMessage && errorMessage.errors"
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
                    <div v-for="(errors, field) in errorMessage.errors" :key="field">
                      <li v-for="(error, index) in errors" :key="index">
                        <strong>{{ field }}:</strong> {{ error }}
                      </li>
                    </div>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <div v-if="success" class="bg-green-50 border border-green-200 rounded-md p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <CheckCircleIcon class="h-5 w-5 text-green-400" />
              </div>
              <div class="ml-3">
                <p class="text-sm text-green-800">{{ success }}</p>
              </div>
            </div>
          </div>

          <div class="space-y-4">
            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div>
                <label for="first_name" class="block text-sm font-medium text-gray-700"
                  >First Name *</label
                >
                <input
                  id="first_name"
                  v-model="form.first_name"
                  type="text"
                  autocomplete="given-name"
                  required
                  class="input-field"
                  placeholder="John"
                />
              </div>

              <div>
                <label for="last_name" class="block text-sm font-medium text-gray-700"
                  >Last Name *</label
                >
                <input
                  id="last_name"
                  v-model="form.last_name"
                  type="text"
                  autocomplete="family-name"
                  required
                  class="input-field"
                  placeholder="Doe"
                />
              </div>
            </div>

            <div>
              <label for="email" class="block text-sm font-medium text-gray-700">Email *</label>
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
              <label for="password" class="block text-sm font-medium text-gray-700"
                >Password *</label
              >
              <input
                id="password"
                v-model="form.password"
                type="password"
                autocomplete="new-password"
                required
                class="input-field"
                placeholder="Create a strong password"
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
            {{ loading ? 'Creating account...' : 'Create Account' }}
          </button>

          <div class="text-center">
            <p class="text-sm text-gray-600">
              Already have an account?
              <NuxtLink
                to="/auth/login"
                class="font-medium text-primary-600 hover:text-primary-500"
              >
                Sign in
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
  import { ExclamationTriangleIcon, CheckCircleIcon } from '@heroicons/vue/24/outline'

  definePageMeta({
    layout: 'auth'
  })

  const authStore = useAuthStore()

  const loading = ref(false)
  const success = ref('')

  const form = ref({
    email: '',
    password: '',
    first_name: '',
    last_name: ''
  })

  const errorMessage = computed(() => {
    const result = authStore.registerResult
    if (!result || result.success) return null

    return {
      message: result.message || 'Please fix the following errors:',
      errors: result.errors || null
    }
  })

  const handleRegister = async () => {
    loading.value = true
    success.value = ''

    try {
      const userData = {
        email: form.value.email,
        password: form.value.password
      }

      if (form.value.first_name) userData.first_name = form.value.first_name
      if (form.value.last_name) userData.last_name = form.value.last_name

      const result = await authStore.register(userData)

      if (result.success) {
        success.value = result.message + ' You can now sign in.'

        form.value = {
          email: '',
          password: '',
          first_name: '',
          last_name: ''
        }

        setTimeout(() => {
          navigateTo('/auth/login')
        }, 2000)
      }
    } catch (err) {
      console.error('Register error:', err)
    } finally {
      loading.value = false
    }
  }
</script>
