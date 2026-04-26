<script setup lang="ts">
const props = defineProps<{
  householdId: number
}>()

const emit = defineEmits<{
  created: []
}>()

const expenseStore = useExpenseStore()
const today = new Date()

const form = reactive({
  description: '',
  merchant: '',
  amount: null as number | null,
  expense_date: today,
})

const successMessage = ref('')
const errorMessage = ref('')
const saving = ref(false)

function toDateInput(date: Date) {
  return date.toISOString().slice(0, 10)
}

function resetForm() {
  form.description = ''
  form.merchant = ''
  form.amount = null
  form.expense_date = new Date()
}

async function submit() {
  errorMessage.value = ''
  successMessage.value = ''

  if (!form.description || !form.amount || !form.expense_date) {
    errorMessage.value = 'Fill in description, amount, and date.'
    return
  }

  saving.value = true

  try {
    await expenseStore.createExpense({
      household: props.householdId,
      description: form.description,
      merchant: form.merchant,
      amount: form.amount,
      expense_date: toDateInput(form.expense_date),
    })

    successMessage.value = 'Expense added successfully.'
    resetForm()
    emit('created')
  } catch {
    errorMessage.value = 'Could not add the expense.'
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <Card>
    <template #title>
      Add expense
    </template>

    <template #subtitle>
      Use this when you want to record a purchase manually, without a receipt.
    </template>

    <template #content>
      <form
        class="form-stack"
        @submit.prevent="submit"
      >
        <Message
          v-if="successMessage"
          severity="success"
        >
          {{ successMessage }}
        </Message>

        <Message
          v-if="errorMessage"
          severity="error"
        >
          {{ errorMessage }}
        </Message>

        <div class="field">
          <label for="expense-description">What was it?</label>
          <InputText
            id="expense-description"
            v-model="form.description"
            placeholder="Example: Weekly groceries"
            required
          />
        </div>

        <div class="form-grid-2">
          <div class="field">
            <label for="expense-amount">Amount</label>
            <InputNumber
              id="expense-amount"
              v-model="form.amount"
              mode="currency"
              currency="BRL"
              locale="pt-BR"
              :min="0"
              required
            />
          </div>

          <div class="field">
            <label for="expense-date">Date</label>
            <DatePicker
              id="expense-date"
              v-model="form.expense_date"
              date-format="yy-mm-dd"
              show-icon
              required
            />
          </div>
        </div>

        <div class="field">
          <label for="expense-merchant">Merchant</label>
          <InputText
            id="expense-merchant"
            v-model="form.merchant"
            placeholder="Example: Whole Foods"
          />
        </div>

        <Button
          type="submit"
          label="Save expense"
          icon="pi pi-plus"
          :loading="saving"
        />
      </form>
    </template>
  </Card>
</template>
