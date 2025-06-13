<template>
  <div></div>
</template>

<script setup>
  definePageMeta({
    middleware: 'auth'
  })

  // This will redirect to dashboard via middleware
  await navigateTo('/dashboard')
</script>
