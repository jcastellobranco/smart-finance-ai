<script setup lang="ts">
definePageMeta({
  middleware: 'auth-client',
})

const auth = useAuthStore()
const expenseStore = useExpenseStore()

const householdId = computed(() => auth.primaryHouseholdId)

onMounted(async () => {
  auth.hydrate()
  if (!auth.user) await auth.fetchMe()

  await Promise.all([
    expenseStore.fetchExpenses(),
    expenseStore.fetchSummary(),
  ])
})
</script>

<template>
  <main class="app-page">
    <div class="app-shell">
      <AppHeader />

      <div class="page-head">
        <div>
          <p class="eyebrow">Dashboard</p>
          <h1 class="page-title">Household financial overview</h1>
          <p class="page-subtitle">
            Track expenses, categories, and processed receipts in one clear workspace.
          </p>
        </div>
      </div>

      <section class="summary-grid">
        <SummaryCard
          title="Total spent"
          :value="`R$ ${expenseStore.summary?.total || 0}`"
          subtitle="Current period"
        />

        <SummaryCard
          title="Categories"
          :value="expenseStore.summary?.by_category.length || 0"
          subtitle="With recorded spending"
        />

        <SummaryCard
          title="Expenses"
          :value="expenseStore.expenses.length"
          subtitle="Recorded"
        />
      </section>

      <section class="dashboard-grid">
        <div>
          <h2 class="section-title">Latest expenses</h2>

          <div
            v-if="expenseStore.expenses.length"
            class="stack"
          >
            <ExpenseCard
              v-for="expense in expenseStore.expenses.slice(0, 6)"
              :key="expense.id"
              :expense="expense"
            />
          </div>

          <div
            v-else
            class="empty-state"
          >
            No expenses recorded yet.
          </div>
        </div>

        <div
          v-if="householdId"
          class="side-stack"
        >
          <ExpenseForm
            :household-id="householdId"
            @created="expenseStore.fetchExpenses"
          />

          <ReceiptUpload
            :household-id="householdId"
            @uploaded="expenseStore.fetchExpenses"
          />
        </div>
      </section>
    </div>
  </main>
</template>
