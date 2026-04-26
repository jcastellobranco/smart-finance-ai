export type ReceiptStatus = 'pending' | 'processing' | 'completed' | 'failed'

export interface ReceiptUpload {
  id: number
  household: number
  uploaded_by: number
  file: string
  status: ReceiptStatus
  raw_text: string
  extracted_data: Record<string, unknown>
  error_message: string
  created_at: string
  processed_at: string | null
}