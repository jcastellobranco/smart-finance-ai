export interface Expense {
  id: number
  household: number
  paid_by: number
  category: number | null
  category_name: string | null
  description: string
  merchant: string
  amount: string
  expense_date: string
  source: 'manual' | 'receipt'
  created_at: string
}

export interface ExpenseSummary {
  total: string | number
  by_category: {
    category__name: string | null
    total: string | number
  }[]
}