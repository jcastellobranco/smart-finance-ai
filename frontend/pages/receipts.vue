<script setup lang="ts">
definePageMeta({
  middleware: 'auth-client',
})

const auth = useAuthStore()
const receiptStore = useReceiptStore()
const householdId = computed(() => auth.primaryHouseholdId)

let intervalId: ReturnType<typeof setInterval> | null = null

onMounted(async () => {
  auth.hydrate()
  if (!auth.user) await auth.fetchMe()

  await receiptStore.fetchReceipts()

  intervalId = setInterval(async () => {
    const pendingReceipts = receiptStore.receipts.filter((receipt) =>
      ['pending', 'processing'].includes(receipt.status)
    )

    await Promise.all(
      pendingReceipts.map((receipt) => receiptStore.refreshReceipt(receipt.id))
    )
  }, 3000)
})

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId)
})
</script>

<template>
  <main class="app-page">
    <div class="app-shell">
      <AppHeader />

      <div class="page-head">
        <div>
          <p class="eyebrow">Receipts</p>
          <h1 class="page-title">Receipt import</h1>
          <p class="page-subtitle">
            Upload files, follow processing status, and review extracted data.
          </p>
        </div>
      </div>

      <section class="receipt-upload-section">
        <ReceiptUpload
          v-if="householdId"
          :household-id="householdId"
          @uploaded="receiptStore.fetchReceipts"
        />

        <Card
          v-else
          class="receipt-upload-card"
        >
          <template #title>
            Upload receipt
          </template>

          <template #subtitle>
            Your workspace is loading. The upload area will appear here.
          </template>

          <template #content>
            <Message
              severity="info"
              :closable="false"
            >
              If this stays here, your account does not have a household workspace attached yet.
            </Message>
          </template>
        </Card>
      </section>

      <div
        v-if="receiptStore.receipts.length"
        class="receipt-list"
      >
        <Card
          v-for="receipt in receiptStore.receipts"
          :key="receipt.id"
        >
          <template #content>
            <div class="receipt-card-head">
              <div>
                <strong>Receipt #{{ receipt.id }}</strong>

                <p class="muted">
                  Criada em {{ receipt.created_at }}
                </p>
              </div>

              <Tag
                :severity="{
                  pending: 'warn',
                  processing: 'info',
                  completed: 'success',
                  failed: 'danger',
                }[receipt.status]"
                :value="receipt.status"
              />
            </div>

            <pre
              v-if="receipt.status === 'completed'"
              class="receipt-json"
            >{{ receipt.extracted_data }}</pre>
          </template>
        </Card>
      </div>

      <div
        v-else
        class="empty-state"
      >
        No receipts uploaded yet.
      </div>
    </div>
  </main>
</template>
