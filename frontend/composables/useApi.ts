import axios from 'axios'

export const useApi = () => {
  const config = useRuntimeConfig()

  const api = axios.create({
    baseURL: config.public.apiBase,
  })

  api.interceptors.request.use((request) => {
    if (import.meta.client) {
      const token = window.sessionStorage.getItem('smart-finance-token')

      if (token) {
        request.headers.Authorization = `Token ${token}`
      }
    }

    return request
  })

  return api
}
