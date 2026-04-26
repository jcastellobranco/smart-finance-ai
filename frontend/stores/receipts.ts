import type { ReceiptUpload } from '~/types/receipt'

export const useReceiptStore = defineStore('receipts', () => {
  const api = useApi()

  const receipts = ref<ReceiptUpload[]>([])
  const loading = ref(false)
  const uploading = ref(false)

  async function fetchReceipts() {
    loading.value = true

    try {
      const { data } = await api.get<ReceiptUpload[]>('/receipts/')
      receipts.value = data
    } finally {
      loading.value = false
    }
  }

  async function uploadReceipt(payload: {
    household: number
    file: File
  }) {
    uploading.value = true

    const formData = new FormData()
    formData.append('household', String(payload.household))
    formData.append('file', payload.file)

    try {
      const { data: receipt } = await api.post<ReceiptUpload>('/receipts/', formData)

      receipts.value.unshift(receipt)

      return receipt
    } finally {
      uploading.value = false
    }
  }

  async function refreshReceipt(id: number) {
    const { data: updated } = await api.get<ReceiptUpload>(`/receipts/${id}/`)

    const index = receipts.value.findIndex((receipt) => receipt.id === id)

    if (index !== -1) {
      receipts.value[index] = updated
    }

    return updated
  }

  return {
    receipts,
    loading,
    uploading,
    fetchReceipts,
    uploadReceipt,
    refreshReceipt,
  }
})
