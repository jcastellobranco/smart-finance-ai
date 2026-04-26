<script setup lang="ts">
definePageMeta({
  middleware: 'auth-client',
})

const expenseStore = useExpenseStore()
const auth = useAuthStore()

const householdId = computed(() => auth.primaryHouseholdId)

onMounted(async () => {
  auth.hydrate()
  if (!auth.user) await auth.fetchMe()
  await expenseStore.fetchExpenses()
})
</script>

<template>
  <main class="app-page">
    <div class="app-shell">
      <AppHeader />

      <div class="page-head">
        <div>
          <p class="eyebrow">Expenses</p>
          <h1 class="page-title">Manual entries</h1>
          <p class="page-subtitle">
            Review everything entered manually or extracted from uploaded receipts.
          </p>
        </div>
      </div>

      <section class="content-grid">
        <ExpenseForm
          v-if="householdId"
          :household-id="householdId"
          @created="expenseStore.fetchExpenses"
        />

        <div>
          <h2 class="section-title">History</h2>

          <div
            v-if="expenseStore.expenses.length"
            class="stack"
          >
            <ExpenseCard
              v-for="expense in expenseStore.expenses"
              :key="expense.id"
              :expense="expense"
            />
          </div>

          <div
            v-else
            class="empty-state"
          >
            No expenses to show.
          </div>
        </div>
      </section>
    </div>
  </main>
</template>
