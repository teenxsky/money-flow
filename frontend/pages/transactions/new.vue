<template>
  <div class="max-w-2xl mx-auto">
    <div class="card">
      <div class="card-header">
        <h3 class="text-lg font-medium text-gray-900">Create New Transaction</h3>
      </div>
      <div class="card-body">
        <form @submit.prevent="createTransaction" class="space-y-6">
          <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label class="block text-sm font-medium text-gray-700">Transaction Type *</label>
              <select
                v-model="form.transaction_type_id"
                class="input-field"
                required
                @change="onTransactionTypeChange"
              >
                <option value="">Select type</option>
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
              <label class="block text-sm font-medium text-gray-700">Status *</label>
              <select v-model="form.status_id" class="input-field" required>
                <option value="">Select status</option>
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
              <label class="block text-sm font-medium text-gray-700">Category *</label>
              <select
                v-model="form.category_id"
                class="input-field"
                required
                @change="onCategoryChange"
                :disabled="!form.transaction_type_id"
              >
                <option value="">Select category</option>
                <option
                  v-for="category in filteredCategories"
                  :key="category.id"
                  :value="category.id"
                >
                  {{ category.name }}
                </option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Subcategory</label>
              <select
                v-model="form.subcategory_id"
                class="input-field"
                :disabled="!form.category_id"
              >
                <option value="">Select subcategory (optional)</option>
                <option
                  v-for="subcategory in filteredSubcategories"
                  :key="subcategory.id"
                  :value="subcategory.id"
                >
                  {{ subcategory.name }}
                </option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Amount *</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <span class="text-gray-500 sm:text-sm">$</span>
              </div>
              <input
                v-model="form.amount"
                type="number"
                step="0.01"
                min="0"
                class="input-field pl-7"
                placeholder="0.00"
                required
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Comment</label>
            <textarea
              v-model="form.comment"
              rows="3"
              class="input-field"
              placeholder="Optional comment about this transaction"
              maxlength="50"
            ></textarea>
            <p class="mt-1 text-sm text-gray-500">{{ form.comment?.length || 0 }}/50 characters</p>
          </div>

          <div class="flex justify-end space-x-3">
            <NuxtLink to="/dashboard" class="btn-secondary">Cancel</NuxtLink>
            <button
              type="submit"
              :disabled="loading"
              class="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span
                v-if="loading"
                class="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"
              ></span>
              {{ loading ? 'Creating...' : 'Create Transaction' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, computed, onMounted } from 'vue'

  definePageMeta({
    middleware: 'auth',
    layout: 'default'
  })

  const transactionsStore = useTransactionsStore()

  const loading = ref(false)
  const form = ref({
    transaction_type_id: '',
    status_id: '',
    category_id: '',
    subcategory_id: '',
    amount: '',
    comment: ''
  })

  const filteredCategories = computed(() => {
    if (!form.value.transaction_type_id) return []
    return transactionsStore.filteredCategories(parseInt(form.value.transaction_type_id))
  })

  const filteredSubcategories = computed(() => {
    if (!form.value.category_id) return []
    return transactionsStore.filteredSubcategories(parseInt(form.value.category_id))
  })

  const onTransactionTypeChange = () => {
    form.value.category_id = ''
    form.value.subcategory_id = ''
  }

  const onCategoryChange = () => {
    form.value.subcategory_id = ''
  }

  const createTransaction = async () => {
    loading.value = true

    try {
      const transactionData = {
        transaction_type_id: parseInt(form.value.transaction_type_id),
        status_id: parseInt(form.value.status_id),
        category_id: parseInt(form.value.category_id),
        amount: form.value.amount.toString()
      }

      if (form.value.subcategory_id) {
        transactionData.subcategory_id = parseInt(form.value.subcategory_id)
      }

      if (form.value.comment) {
        transactionData.comment = form.value.comment
      }

      await transactionsStore.createTransaction(transactionData)

      // Reset form
      form.value = {
        transaction_type_id: '',
        status_id: '',
        category_id: '',
        subcategory_id: '',
        amount: '',
        comment: ''
      }

      // Redirect to dashboard
      await navigateTo('/dashboard')
    } catch (error) {
      console.error('Create transaction error:', error)
      alert('Failed to create transaction. Please try again.')
    } finally {
      loading.value = false
    }
  }

  onMounted(async () => {
    try {
      await transactionsStore.fetchMetadata()
    } catch (error) {
      console.error('Failed to load metadata:', error)
      alert('Failed to load form data')
    }
  })
</script>
