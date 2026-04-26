<script setup lang="ts">
defineProps<{
  title: string
  value: string | number
  subtitle?: string
}>()
</script>

<template>
  <Card>
    <template #content>
      <p class="muted">{{ title }}</p>
      <p class="amount">{{ value }}</p>
      <p
        v-if="subtitle"
        class="tiny"
      >
        {{ subtitle }}
      </p>
    </template>
  </Card>
</template>
