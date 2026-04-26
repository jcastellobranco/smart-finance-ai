import { defineStore } from 'pinia'
import type { Expense, ExpenseSummary } from '~/types/expense'

export const useExpenseStore = defineStore('expenses', {
  state: () => ({
    expenses: [] as Expense[],
    summary: null as ExpenseSummary | null,
    loading: false,
  }),

  actions: {
    async fetchExpenses() {
      const api = useApi()
      this.loading = true

      try {
        const { data } = await api.get('/expenses/')
        this.expenses = data
      } finally {
        this.loading = false
      }
    },

    async fetchSummary() {
      const api = useApi()
      const { data } = await api.get('/expenses/summary/')

      this.summary = data
    },

    async createExpense(payload: any) {
      const api = useApi()
      const { data } = await api.post('/expenses/', payload)

      this.expenses.unshift(data)
      await this.fetchSummary()

      return data
    }
  }
})
