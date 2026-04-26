<script setup lang="ts">
import type { Expense } from '~/types/expense'

defineProps<{
  expense: Expense
}>()
</script>

<template>
  <Card>
    <template #content>
      <div class="expense-row">
      <div>
        <strong>
          {{ expense.description }}
        </strong>

        <p class="muted">
          {{ expense.merchant || 'No merchant' }}
        </p>

        <p class="tiny">
          {{ expense.category_name || 'Uncategorized' }} · {{ expense.expense_date }}
        </p>
      </div>

      <div>
        <p class="amount">
          R$ {{ expense.amount }}
        </p>

        <Tag
          :severity="expense.source === 'receipt' ? 'info' : 'secondary'"
          :value="expense.source === 'receipt' ? 'Receipt' : 'Manual'"
        />
      </div>
      </div>
    </template>
  </Card>
</template>
