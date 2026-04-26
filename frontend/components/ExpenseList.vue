<script setup>
import { onMounted } from 'vue'
import { useExpenseStore } from '@/stores/expenses'

const store = useExpenseStore()

onMounted(() => {
  store.fetchExpenses()
})
</script>

<template>
  <div class="p-4">
    <h2 class="text-xl mb-4">Expenses</h2>

    <DataTable :value="store.expenses" :loading="store.loading">
      <Column field="description" header="Description" />
      <Column field="amount" header="Amount" />
      <Column field="merchant" header="Merchant" />
      <Column field="expense_date" header="Date" />
    </DataTable>
  </div>
</template>