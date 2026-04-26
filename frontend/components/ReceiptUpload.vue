<script setup lang="ts">
const props = defineProps<{
  householdId: number
}>()

const emit = defineEmits<{
  uploaded: []
}>()

const receiptStore = useReceiptStore()
const file = ref<File | null>(null)
const errorMessage = ref('')
const successMessage = ref('')

function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  file.value = input.files?.[0] ?? null
  errorMessage.value = ''
  successMessage.value = ''
}

async function upload() {
  if (!file.value) {
    errorMessage.value = 'Selecione um arquivo para enviar.'
    return
  }

  try {
    await receiptStore.uploadReceipt({
      household: props.householdId,
      file: file.value,
    })

    file.value = null
    successMessage.value = 'Receipt uploaded. Processing status appears in the receipts list.'
    emit('uploaded')
  } catch {
    errorMessage.value = 'Could not upload the receipt.'
  }
}
</script>

<template>
  <Card class="receipt-upload-card">
    <template #title>
      Upload receipt
    </template>

    <template #subtitle>
      Use this when you have a PDF or photo and want the backend to process it.
    </template>

    <template #content>
      <div class="form-stack">
        <div class="receipt-dropzone">
          <input
            id="receipt-file"
            class="receipt-file-input"
            type="file"
            accept="image/*,.pdf"
            @change="onFileChange"
          >

          <label
            class="receipt-file-label"
            for="receipt-file"
          >
            <i class="pi pi-cloud-upload" />
            <span>
              <strong>{{ file?.name || 'Choose receipt file' }}</strong>
              <small>PDF, JPG, or PNG</small>
            </span>
          </label>
        </div>

        <div class="upload-actions">
          <Button
            type="button"
            label="Upload"
            icon="pi pi-upload"
            :loading="receiptStore.uploading"
            @click="upload"
          />

          <span
            v-if="file"
            class="tiny"
          >
            Ready to upload
          </span>
        </div>

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
      </div>
    </template>
  </Card>
</template>
