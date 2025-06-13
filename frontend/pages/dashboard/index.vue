<template>
  <div class="space-y-6">
    <transition name="fade">
      <div
        v-if="isLoading"
        class="absolute inset-0 bg-white bg-opacity-100 z-50 flex items-center justify-center"
      >
        <div class="text-center">
          <div
            class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"
          ></div>
        </div>
      </div>
    </transition>
    <div class="flex items-center justify-end space-x-4 mr-6 mt-4">
      <div v-if="authStore.user" class="flex items-center space-x-2 group">
        <div class="text-right hidden sm:block">
          <div class="text-xs text-gray-500">Welcome back</div>
          <div
            class="text-sm font-medium text-gray-700 group-hover:text-primary-600 transition-colors"
          >
            {{ authStore.user.first_name }} {{ authStore.user.last_name }}
          </div>
        </div>
        <div class="relative">
          <div
            class="w-8 h-8 rounded-full bg-gradient-to-br from-primary-100 to-primary-200 flex items-center justify-center border border-primary-200 shadow-sm"
          >
            <span class="text-xs font-medium text-primary-700 uppercase">
              {{ authStore.user.first_name.charAt(0) }}{{ authStore.user.last_name.charAt(0) }}
            </span>
          </div>
          <div
            class="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-green-400 rounded-full border-2 border-white"
          ></div>
        </div>
      </div>
      <button @click="logout" class="btn-secondary inline-flex items-center group" title="Logout">
        <ArrowRightOnRectangleIcon
          class="w-4 h-4 mr-2 group-hover:text-red-500 transition-colors"
        />
        <span class="hidden sm:inline">Logout</span>
      </button>
    </div>
    <!-- Stats Cards -->
    <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 px-4 sm:px-6">
      <div class="card">
        <div class="card-body">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                <ArrowUpIcon class="w-5 h-5 text-green-600" />
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Total Income</dt>
                <dd class="text-lg font-medium text-gray-900">${{ totalIncome }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center">
                <ArrowDownIcon class="w-5 h-5 text-red-600" />
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Total Expenses</dt>
                <dd class="text-lg font-medium text-gray-900">${{ totalExpenses }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                <BanknotesIcon class="w-5 h-5 text-blue-600" />
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Net Balance</dt>
                <dd class="text-lg font-medium text-gray-900">${{ netBalance }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                <DocumentTextIcon class="w-5 h-5 text-purple-600" />
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Total Transactions</dt>
                <dd class="text-lg font-medium text-gray-900">
                  {{ transactionsStore.transactions.length }}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="card">
      <div class="card-header">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900">Filters</h3>
          <button @click="clearFilters" class="text-sm text-primary-600 hover:text-primary-700">
            Clear All
          </button>
        </div>
      </div>
      <div class="card-body">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-6">
          <div>
            <label class="block text-sm font-medium text-gray-700">Date From</label>
            <input
              v-model="filters.created_at__gte"
              type="date"
              class="input-field"
              @change="applyFilters"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Date To</label>
            <input
              v-model="filters.created_at__lte"
              type="date"
              class="input-field"
              @change="applyFilters"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Transaction Type</label>
            <select v-model="filters.transaction_type" class="input-field" @change="applyFilters">
              <option value="">All Types</option>
              <option
                v-for="type in transactionsStore.transactionTypes"
                :key="type.id"
                :value="type.id"
              >
                {{ type.name }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Status</label>
            <select v-model="filters.status" class="input-field" @change="applyFilters">
              <option value="">All Statuses</option>
              <option
                v-for="status in transactionsStore.statuses"
                :key="status.id"
                :value="status.id"
              >
                {{ status.name }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Sort By</label>
            <select v-model="filters.sort_field" class="input-field" @change="applyFilters">
              <option value="created_at">Date</option>
              <option value="amount">Amount</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Order</label>
            <select v-model="filters.sort_order" class="input-field" @change="applyFilters">
              <option value="desc">Descending</option>
              <option value="asc">Ascending</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Transactions Table -->
    <div class="card">
      <div class="card-header">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900">Recent Transactions</h3>
          <NuxtLink to="/transactions/new" class="btn-primary inline-flex items-center">
            <PlusIcon class="w-4 h-4 mr-2" />New Transaction
          </NuxtLink>
        </div>
      </div>
      <div class="card-body p-0">
        <div v-if="transactionsStore.loading" class="text-center py-8">
          <div
            class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"
          ></div>
          <p class="mt-2 text-sm text-gray-500">Loading transactions...</p>
        </div>

        <div v-else-if="transactionsStore.transactions.length === 0" class="text-center py-8">
          <DocumentTextIcon class="mx-auto h-12 w-12 text-gray-400" />
          <h3 class="mt-2 text-sm font-medium text-gray-900">No transactions</h3>
          <p class="mt-1 text-sm text-gray-500">Get started by creating a new transaction.</p>
          <div class="mt-6">
            <NuxtLink to="/transactions/new" class="btn-primary inline-flex items-center">
              <PlusIcon class="w-4 h-4 mr-2" />New Transaction
            </NuxtLink>
          </div>
        </div>

        <div v-else class="overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Date
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Type
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Category
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Amount
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Status
                </th>
                <th
                  class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr
                v-for="transaction in transactionsStore.transactions"
                :key="transaction.id"
                class="table-row"
              >
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ formatDate(transaction.created_at) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ transaction.transaction_type_name }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">
                    {{ transaction.category_name }}
                  </div>
                  <div v-if="transaction.subcategory_name" class="text-sm text-gray-500">
                    {{ transaction.subcategory_name }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <span :class="getAmountClass(transaction.transaction_type_name)">
                    ${{ Math.abs(parseFloat(transaction.amount)).toFixed(2) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="getStatusBadgeClass(transaction.status_name)">
                    {{ transaction.status_name }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button
                    @click="deleteTransaction(transaction.id)"
                    class="text-red-600 hover:text-red-900 transition-colors duration-200"
                  >
                    <TrashIcon class="w-4 h-4" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, computed, onMounted } from 'vue'
  import {
    ArrowUpIcon,
    ArrowDownIcon,
    BanknotesIcon,
    DocumentTextIcon,
    PlusIcon,
    TrashIcon,
    ArrowRightOnRectangleIcon
  } from '@heroicons/vue/24/outline'

  definePageMeta({
    middleware: 'auth',
    layout: 'default'
  })

  const isLoading = ref(true)

  const transactionsStore = useTransactionsStore()
  const authStore = useAuthStore()

  const logout = async () => {
    await authStore.logout()
    await navigateTo('/auth/login')
  }

  const filters = ref({
    created_at__gte: '',
    created_at__lte: '',
    transaction_type: '',
    status: '',
    sort_field: 'created_at',
    sort_order: 'desc'
  })

  const totalIncome = computed(() => {
    return transactionsStore.transactions
      .filter(t => t.transaction_type_name.toLowerCase().includes('income'))
      .reduce((sum, t) => sum + parseFloat(t.amount), 0)
      .toFixed(2)
  })

  const totalExpenses = computed(() => {
    return Math.abs(
      transactionsStore.transactions
        .filter(t => t.transaction_type_name.toLowerCase().includes('expense'))
        .reduce((sum, t) => sum + parseFloat(t.amount), 0)
    ).toFixed(2)
  })

  const netBalance = computed(() => {
    return (parseFloat(totalIncome.value) - parseFloat(totalExpenses.value)).toFixed(2)
  })

  const formatDate = dateString => {
    return new Date(dateString).toLocaleString()
  }

  const getAmountClass = transactionType => {
    if (transactionType.toLowerCase().includes('income')) {
      return 'text-green-600'
    } else if (transactionType.toLowerCase().includes('expense')) {
      return 'text-red-600'
    }
    return 'text-gray-900'
  }

  const getStatusBadgeClass = status => {
    const baseClass = 'badge'
    switch (status.toLowerCase()) {
      case 'completed':
      case 'success':
        return `${baseClass} badge-success`
      case 'pending':
        return `${baseClass} badge-warning`
      case 'failed':
      case 'cancelled':
        return `${baseClass} badge-danger`
      default:
        return `${baseClass} badge-info`
    }
  }

  const applyFilters = () => {
    const cleanFilters = {}
    Object.entries(filters.value).forEach(([key, value]) => {
      if (value !== null && value !== '') {
        cleanFilters[key] = value
      }
    })

    if (cleanFilters.sort_field) {
      cleanFilters.ordering =
        (cleanFilters.sort_order === 'asc' ? '' : '-') + cleanFilters.sort_field
      delete cleanFilters.sort_field
      delete cleanFilters.sort_order
    }

    transactionsStore.setFilters(cleanFilters)
    transactionsStore.fetchTransactions()
  }

  const clearFilters = () => {
    filters.value = {
      created_at__gte: '',
      created_at__lte: '',
      transaction_type: '',
      status: '',
      sort_field: 'created_at',
      sort_order: 'desc'
    }
    transactionsStore.clearFilters()
    transactionsStore.fetchTransactions()
  }

  const deleteTransaction = async id => {
    if (confirm('Are you sure you want to delete this transaction?')) {
      try {
        await transactionsStore.deleteTransaction(id)
      } catch (error) {
        console.error('Delete transaction error:', error)
        alert('Failed to delete transaction')
      }
    }
  }

  onMounted(async () => {
    try {
      isLoading.value = true
      if (!authStore.isAuthenticated) {
        await authStore.initializeAuth()
      }

      await transactionsStore.fetchMetadata()
      await transactionsStore.fetchTransactions()
      isLoading.value = false
    } catch (error) {
      isLoading.value = false
      console.error('Failed to load dashboard data:', error)
    }
  })
</script>
