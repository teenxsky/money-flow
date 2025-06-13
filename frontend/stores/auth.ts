import { defineStore } from 'pinia'
import { FetchError } from 'ofetch'

interface User {
  id: number
  email: string
  first_name: string
  last_name: string
}

interface AuthResult {
  success: boolean
  message: string
  error?: string | null
  errors?: Record<string, string[]> | null
}

interface AuthState {
  user: User | null
  token: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  loginResult: AuthResult | null
  registerResult: AuthResult | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: null,
    refreshToken: null,
    isAuthenticated: false,
    loginResult: null,
    registerResult: null
  }),

  actions: {
    async requestWithAuth<T>(request: () => Promise<T>): Promise<T> {
      try {
        return await request()
      } catch (error: unknown) {
        if (this.isAuthError(error)) {
          const refreshSuccessful = await this.refreshTokens()
          if (refreshSuccessful) {
            return await request()
          }
          await this.logout()
          throw error
        }
        throw error
      }
    },

    isAuthError(error: unknown): boolean {
      return error instanceof FetchError && error.status === 401
    },

    async login(email: string, password: string) {
      const config = useRuntimeConfig()

      try {
        const response = await $fetch<{
          message: string
          access: string
          refresh: string
        }>(`${config.public.apiBase}/v1/users/login/`, {
          method: 'POST',
          body: { email, password }
        })

        this.token = response.access
        this.refreshToken = response.refresh
        this.isAuthenticated = true
        this.loginResult = {
          success: true,
          message: response.message,
          error: null,
          errors: null
        }

        if (process.client) {
          localStorage.setItem('auth_token', response.access)
          localStorage.setItem('refresh_token', response.refresh)
        }

        await this.fetchUser()

        return this.loginResult
      } catch (error: any) {
        const errorData = error.data || {}
        this.loginResult = {
          success: false,
          message: errorData.message || 'Login failed',
          error: errorData.error || null,
          errors: errorData.errors || null
        }
        return this.loginResult
      }
    },

    async register(userData: {
      email: string
      password: string
      first_name?: string
      last_name?: string
    }) {
      const config = useRuntimeConfig()

      try {
        const response = await $fetch<{ message: string }>(
          `${config.public.apiBase}/v1/users/register/`,
          {
            method: 'POST',
            body: userData
          }
        )

        this.registerResult = {
          success: true,
          message: response.message,
          errors: null
        }

        return this.registerResult
      } catch (error: any) {
        console.error('Registration error:', error)
        const errorData = error.data || {}

        this.registerResult = {
          success: false,
          message: errorData.message || 'Registration failed',
          errors: this.normalizeRegisterErrors(errorData)
        }

        return this.registerResult
      }
    },

    normalizeRegisterErrors(errorData: any): Record<string, string[]> | null {
      if (!errorData) return null

      if (typeof errorData === 'object') {
        const result: Record<string, string[]> = {}

        for (const [field, messages] of Object.entries(errorData['error'])) {
          if (Array.isArray(messages)) {
            result[field] = messages
          } else if (typeof messages === 'string') {
            result[field] = [messages]
          } else if (typeof messages === 'object') {
            result[field] = Object.values(messages as Record<string, string[]>).flat() as string[]
          }
        }

        console.log(result)

        return Object.keys(result).length > 0 ? result : null
      }

      return null
    },

    async logout() {
      const config = useRuntimeConfig()

      try {
        if (this.refreshToken) {
          await this.requestWithAuth(() =>
            $fetch(`${config.public.apiBase}/v1/users/logout/`, {
              method: 'POST',
              body: { refresh: this.refreshToken }
            })
          )
        }
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        this.clearAuthState()
        await navigateTo('/auth/login')
      }
    },

    async fetchUser(): Promise<void> {
      if (!this.token) return

      const config = useRuntimeConfig()

      return this.requestWithAuth(async () => {
        const user = await $fetch<User>(`${config.public.apiBase}/v1/users/me/`, {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        })

        this.user = user
      }).catch(async (error: unknown) => {
        console.error('Fetch user error:', error)
        if (!(await this.refreshTokens())) {
          await this.logout()
        }
        this.fetchUser()
      })
    },

    async refreshTokens() {
      if (!this.refreshToken) return false

      const config = useRuntimeConfig()

      try {
        const response = await $fetch<{ access: string }>(
          `${config.public.apiBase}/v1/users/refresh/`,
          {
            method: 'POST',
            body: { refresh: this.refreshToken }
          }
        )

        this.token = response.access
        this.isAuthenticated = true

        if (process.client) {
          localStorage.setItem('auth_token', response.access)
        }

        return true
      } catch (error) {
        console.error('Token refresh error:', error)
        return false
      }
    },

    async initializeAuth() {
      if (process.client) {
        const token = localStorage.getItem('auth_token')
        const refreshToken = localStorage.getItem('refresh_token')

        if (token && refreshToken) {
          this.token = token
          this.refreshToken = refreshToken
          this.isAuthenticated = true
          await this.fetchUser()
        }
      }
    },

    clearAuthState() {
      this.user = null
      this.token = null
      this.refreshToken = null
      this.isAuthenticated = false

      if (process.client) {
        localStorage.removeItem('auth_token')
        localStorage.removeItem('refresh_token')
      }
    }
  }
})
