<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Mobile sidebar -->
    <TransitionRoot as="template" :show="sidebarOpen">
      <Dialog as="div" class="relative z-50 lg:hidden" @close="sidebarOpen = false">
        <TransitionChild
          as="template"
          enter="transition-opacity ease-linear duration-300"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="transition-opacity ease-linear duration-300"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-gray-900/80" />
        </TransitionChild>

        <div class="fixed inset-0 flex">
          <TransitionChild
            as="template"
            enter="transition ease-in-out duration-300 transform"
            enter-from="-translate-x-full"
            enter-to="translate-x-0"
            leave="transition ease-in-out duration-300 transform"
            leave-from="translate-x-0"
            leave-to="-translate-x-full"
          >
            <DialogPanel class="relative mr-16 flex w-full max-w-xs flex-1">
              <TransitionChild
                as="template"
                enter="ease-in-out duration-300"
                enter-from="opacity-0"
                enter-to="opacity-100"
                leave="ease-in-out duration-300"
                leave-from="opacity-100"
                leave-to="opacity-0"
              >
                <div class="absolute left-full top-0 flex w-16 justify-center pt-5">
                  <button type="button" class="-m-2.5 p-2.5" @click="sidebarOpen = false">
                    <span class="sr-only">Close sidebar</span>
                    <XMarkIcon class="h-6 w-6 text-white" aria-hidden="true" />
                  </button>
                </div>
              </TransitionChild>

              <div class="flex grow flex-col gap-y-5 overflow-y-auto bg-white px-6 pb-4">
                <div class="flex h-16 shrink-0 items-center">
                  <h1 class="text-xl font-bold text-gray-900">Money Flow</h1>
                </div>
                <nav class="flex flex-1 flex-col">
                  <ul role="list" class="flex flex-1 flex-col gap-y-7">
                    <li>
                      <ul role="list" class="-mx-2 space-y-1">
                        <li v-for="item in navigation" :key="item.name">
                          <NuxtLink
                            :to="item.href"
                            :class="[
                              $route.path === item.href
                                ? 'bg-gray-50 text-primary-600'
                                : 'text-gray-700 hover:text-primary-600 hover:bg-gray-50',
                              'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold'
                            ]"
                          >
                            <component
                              :is="item.icon"
                              :class="[
                                $route.path === item.href
                                  ? 'text-primary-600'
                                  : 'text-gray-400 group-hover:text-primary-600',
                                'h-6 w-6 shrink-0'
                              ]"
                              aria-hidden="true"
                            />
                            {{ item.name }}
                          </NuxtLink>
                        </li>
                      </ul>
                    </li>
                  </ul>
                </nav>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </Dialog>
    </TransitionRoot>

    <!-- Static sidebar for desktop -->
    <div class="hidden lg:fixed lg:inset-y-0 lg:z-50 lg:flex lg:w-72 lg:flex-col">
      <div
        class="flex grow flex-col gap-y-5 overflow-y-auto border-r border-gray-200 bg-white px-6 pb-4"
      >
        <div class="flex h-16 shrink-0 items-center">
          <h1 class="text-xl font-bold text-gray-900">Money Flow</h1>
        </div>
        <nav class="flex flex-1 flex-col">
          <ul role="list" class="flex flex-1 flex-col gap-y-7">
            <li>
              <ul role="list" class="-mx-2 space-y-1">
                <li v-for="item in navigation" :key="item.name">
                  <NuxtLink
                    :to="item.href"
                    :class="[
                      $route.path === item.href
                        ? 'bg-gray-50 text-primary-600'
                        : 'text-gray-700 hover:text-primary-600 hover:bg-gray-50',
                      'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold transition-colors duration-200'
                    ]"
                  >
                    <component
                      :is="item.icon"
                      :class="[
                        $route.path === item.href
                          ? 'text-primary-600'
                          : 'text-gray-400 group-hover:text-primary-600',
                        'h-6 w-6 shrink-0'
                      ]"
                      aria-hidden="true"
                    />
                    {{ item.name }}
                  </NuxtLink>
                </li>
              </ul>
            </li>
            <li class="mt-auto">
              <div
                class="flex items-center gap-x-4 px-2 py-3 text-sm font-semibold leading-6 text-gray-900"
              >
                <div class="h-8 w-8 rounded-full bg-gray-50 flex items-center justify-center">
                  <UserIcon class="h-5 w-5 text-gray-400" />
                </div>
                <span class="sr-only">Your profile</span>
                <div class="flex-1">
                  <p class="text-sm text-gray-900">
                    {{ authStore.user?.first_name || authStore.user?.email }}
                  </p>
                </div>
                <button @click="authStore.logout()" class="text-gray-400 hover:text-red-600">
                  <ArrowRightOnRectangleIcon class="h-5 w-5" />
                </button>
              </div>
            </li>
          </ul>
        </nav>
      </div>
    </div>

    <div class="lg:pl-72">
      <div
        class="sticky top-0 z-40 flex h-16 shrink-0 items-center gap-x-4 border-b border-gray-200 bg-white px-4 shadow-sm sm:gap-x-6 sm:px-6 lg:px-8"
      >
        <button
          type="button"
          class="-m-2.5 p-2.5 text-gray-700 lg:hidden"
          @click="sidebarOpen = true"
        >
          <span class="sr-only">Open sidebar</span>
          <Bars3Icon class="h-6 w-6" aria-hidden="true" />
        </button>

        <div class="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
          <div class="flex items-center gap-x-4 lg:gap-x-6">
            <h1 class="text-xl font-semibold leading-6 text-gray-900">
              {{ pageTitle }}
            </h1>
          </div>
        </div>
      </div>

      <main class="py-10">
        <div class="px-4 sm:px-6 lg:px-8">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
  import { ref, computed } from 'vue'
  import { Dialog, DialogPanel, TransitionChild, TransitionRoot } from '@headlessui/vue'
  import {
    Bars3Icon,
    ChartBarIcon,
    PlusIcon,
    UserIcon,
    XMarkIcon,
    ArrowRightOnRectangleIcon
  } from '@heroicons/vue/24/outline'

  const authStore = useAuthStore()
  const route = useRoute()

  const sidebarOpen = ref(false)

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: ChartBarIcon },
    { name: 'New Transaction', href: '/transactions/new', icon: PlusIcon }
  ]

  const pageTitle = computed(() => {
    const currentNav = navigation.find(item => item.href === route.path)
    return currentNav?.name || 'Dashboard'
  })
</script>
