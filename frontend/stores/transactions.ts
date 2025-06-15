import { defineStore } from 'pinia'

interface TransactionType {
  id: number
  name: string
}

interface Category {
  id: number
  name: string
  transaction_type_id: number
}

interface Subcategory {
  id: number
  name: string
  category_id: number
}

interface Status {
  id: number
  name: string
}

interface Transaction {
  id: number
  created_at: string
  updated_at: string
  status_id: string
  status_name: string
  transaction_type_id: string
  transaction_type_name: string
  category_id: string
  category_name: string
  subcategory_id: string | null
  subcategory_name: string | null
  amount: string
  comment: string | null
}

interface TransactionDetail extends Transaction {
  user_email: string
}

interface TransactionFilters {
  created_at__gte?: string
  created_at__lte?: string
  status?: number
  transaction_type?: number
  category?: number
  subcategory?: number
  amount__gte?: number
  amount__lte?: number
  ordering?: string
}

interface TransactionState {
  transactions: Transaction[]
  transactionTypes: TransactionType[]
  categories: Category[]
  subcategories: Subcategory[]
  statuses: Status[]
  filters: TransactionFilters
  loading: boolean
}

export const useTransactionsStore = defineStore('transactions', {
  state: (): TransactionState => ({
    transactions: [],
    transactionTypes: [],
    categories: [],
    subcategories: [],
    statuses: [],
    filters: {},
    loading: false
  }),

  getters: {
    filteredCategories: state => (transactionTypeId?: number) => {
      if (!transactionTypeId) return state.categories
      return state.categories.filter(cat => cat.transaction_type_id === transactionTypeId)
    },

    filteredSubcategories: state => (categoryId?: number) => {
      if (!categoryId) return state.subcategories
      return state.subcategories.filter(sub => sub.category_id === categoryId)
    }
  },

  actions: {
    async fetchTransactions() {
      const authStore = useAuthStore()
      this.loading = true
      const config = useRuntimeConfig()

      try {
        return await authStore.requestWithAuth(async () => {
          const params = new URLSearchParams()
          Object.entries(this.filters).forEach(([key, value]) => {
            if (value !== undefined && value !== null && value !== '') {
              params.append(key, String(value))
            }
          })

          const url = `${config.public.apiBase}/v1/transactions/?${params.toString()}`

          const transactions = await $fetch<Transaction[]>(url, {
            headers: {
              Authorization: `Bearer ${authStore.token}`
            }
          })

          this.transactions = transactions
          return transactions
        })
      } catch (error) {
        console.error('Fetch transactions error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchTransactionById(id: number) {
      const authStore = useAuthStore()
      const config = useRuntimeConfig()

      try {
        return await authStore.requestWithAuth(async () => {
          const transaction = await $fetch<TransactionDetail>(
            `${config.public.apiBase}/v1/transactions/${id}/`,
            {
              headers: {
                Authorization: `Bearer ${authStore.token}`
              }
            }
          )
          return transaction
        })
      } catch (error) {
        console.error('Fetch transaction error:', error)
        throw error
      }
    },

    async fetchMetadata() {
      const config = useNuxtApp().$config

      try {
        const [transactionTypes, categories, subcategories, statuses] = await Promise.all([
          $fetch<TransactionType[]>(`${config.public.apiBase}/v1/transaction-types/`),
          $fetch<Category[]>(`${config.public.apiBase}/v1/categories/`),
          $fetch<Subcategory[]>(`${config.public.apiBase}/v1/subcategories/`),
          $fetch<Status[]>(`${config.public.apiBase}/v1/statuses/`)
        ])

        this.transactionTypes = transactionTypes
        this.categories = categories
        this.subcategories = subcategories
        this.statuses = statuses
      } catch (error) {
        console.error('Fetch metadata error:', error)
        throw error
      }
    },

    async createTransaction(transactionData: {
      status_id: number
      transaction_type_id: number
      category_id: number
      subcategory_id?: number
      amount: string
      comment?: string
    }) {
      const authStore = useAuthStore()
      const config = useRuntimeConfig()

      try {
        const transaction = await $fetch<TransactionDetail>(
          `${config.public.apiBase}/v1/transactions/`,
          {
            method: 'POST',
            headers: {
              Authorization: `Bearer ${authStore.token}`
            },
            body: transactionData
          }
        )

        await this.fetchTransactions()
        return transaction
      } catch (error) {
        console.error('Create transaction error:', error)
        throw error
      }
    },

    async updateTransaction(
      id: number,
      transactionData: {
        status_id?: number
        transaction_type_id?: number
        category_id?: number
        subcategory_id?: number | null
        amount?: string
        comment?: string
      }
    ) {
      const authStore = useAuthStore()
      const config = useRuntimeConfig()

      try {
        const transaction = await $fetch<TransactionDetail>(
          `${config.public.apiBase}/v1/transactions/${id}/`,
          {
            method: 'PATCH',
            headers: {
              Authorization: `Bearer ${authStore.token}`
            },
            body: transactionData
          }
        )

        await this.fetchTransactions()
        return transaction
      } catch (error) {
        console.error('Update transaction error:', error)
        throw error
      }
    },

    async deleteTransaction(id: number) {
      const authStore = useAuthStore()
      const config = useRuntimeConfig()

      try {
        await $fetch(`${config.public.apiBase}/v1/transactions/${id}/`, {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${authStore.token}`
          }
        })

        await this.fetchTransactions()
      } catch (error) {
        console.error('Delete transaction error:', error)
        throw error
      }
    },

    setFilters(filters: TransactionFilters) {
      this.filters = { ...filters }
    },

    clearFilters() {
      this.filters = {}
    }
  }
})
