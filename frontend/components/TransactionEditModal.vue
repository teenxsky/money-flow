<template>
  <TransitionRoot as="template" :show="isOpen">
    <Dialog as="div" class="relative z-50" @close="closeModal">
      <TransitionChild
        as="template"
        enter="ease-out duration-300"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="ease-in duration-200"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
      </TransitionChild>

      <div class="fixed inset-0 z-10 overflow-y-auto">
        <div
          class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0"
        >
          <TransitionChild
            as="template"
            enter="ease-out duration-300"
            enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to="opacity-100 translate-y-0 sm:scale-100"
            leave="ease-in duration-200"
            leave-from="opacity-100 translate-y-0 sm:scale-100"
            leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <DialogPanel
              class="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6"
            >
              <div>
                <div class="mt-3 text-center sm:mt-0 sm:text-left">
                  <DialogTitle as="h3" class="text-lg font-semibold leading-6 text-gray-900">
                    Edit Transaction
                  </DialogTitle>

                  <div class="mt-6">
                    <form @submit.prevent="updateTransaction" class="space-y-4">
                      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                        <div>
                          <label class="block text-sm font-medium text-gray-700"
                            >Transaction Type *</label
                          >
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
                          <div
                            class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
                          >
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
                        <p class="mt-1 text-sm text-gray-500">
                          {{ form.comment?.length || 0 }}/50 characters
                        </p>
                      </div>

                      <div
                        class="mt-5 sm:mt-6 sm:grid sm:grid-flow-row-dense sm:grid-cols-2 sm:gap-3"
                      >
                        <button
                          type="submit"
                          :disabled="loading"
                          class="inline-flex w-full justify-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600 disabled:opacity-50 disabled:cursor-not-allowed sm:col-start-2"
                        >
                          <span
                            v-if="loading"
                            class="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"
                          ></span>
                          {{ loading ? 'Updating...' : 'Update Transaction' }}
                        </button>
                        <button
                          type="button"
                          class="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:col-start-1 sm:mt-0"
                          @click="closeModal"
                        >
                          Cancel
                        </button>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
  import { ref, computed, watch } from 'vue'
  import {
    Dialog,
    DialogPanel,
    DialogTitle,
    TransitionChild,
    TransitionRoot
  } from '@headlessui/vue'

  const props = defineProps({
    isOpen: {
      type: Boolean,
      required: true
    },
    transactionId: {
      type: Number,
      default: null
    }
  })

  const emit = defineEmits(['close', 'updated'])

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

  const loadTransaction = async () => {
    if (!props.transactionId) return

    try {
      loading.value = true
      const transaction = await transactionsStore.fetchTransactionById(props.transactionId)

      form.value = {
        transaction_type_id: transaction.transaction_type_id,
        status_id: transaction.status_id,
        category_id: transaction.category_id,
        subcategory_id: transaction.subcategory_id || '',
        amount: transaction.amount,
        comment: transaction.comment || ''
      }
    } catch (error) {
      console.error('Failed to load transaction:', error)
      alert('Failed to load transaction details')
    } finally {
      loading.value = false
    }
  }

  const updateTransaction = async () => {
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
      } else {
        transactionData.subcategory_id = null
      }

      if (form.value.comment) {
        transactionData.comment = form.value.comment
      }

      await transactionsStore.updateTransaction(props.transactionId, transactionData)

      emit('updated')
      closeModal()
    } catch (error) {
      console.error('Update transaction error:', error)
      alert('Failed to update transaction. Please try again.')
    } finally {
      loading.value = false
    }
  }

  const closeModal = () => {
    emit('close')
    // Reset form
    form.value = {
      transaction_type_id: '',
      status_id: '',
      category_id: '',
      subcategory_id: '',
      amount: '',
      comment: ''
    }
  }

  watch(
    () => props.isOpen,
    isOpen => {
      if (isOpen && props.transactionId) {
        loadTransaction()
      }
    }
  )
</script>
