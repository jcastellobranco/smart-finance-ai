type HouseholdSummary = {
  id: number
  name: string
  role: string
}

type User = {
  id: number
  username: string
  email: string
  households: HouseholdSummary[]
}

type AuthResponse = {
  token: string
  user: User
}

const tokenKey = 'smart-finance-token'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: '' as string,
    user: null as User | null,
    loading: false,
    error: '',
  }),

  getters: {
    isAuthenticated: (state) => Boolean(state.token),
    primaryHouseholdId: (state) => state.user?.households?.[0]?.id ?? null,
  },

  actions: {
    hydrate() {
      if (!import.meta.client) return

      this.token = window.sessionStorage.getItem(tokenKey) || ''
    },

    persist(token: string) {
      this.token = token

      if (import.meta.client) {
        window.sessionStorage.setItem(tokenKey, token)
      }
    },

    clear() {
      this.token = ''
      this.user = null

      if (import.meta.client) {
        window.sessionStorage.removeItem(tokenKey)
        window.localStorage.removeItem(tokenKey)
      }
    },

    async fetchMe() {
      if (!this.token) return

      const api = useApi()
      const { data } = await api.get<User>('/accounts/me/')
      this.user = data
    },

    async login(payload: { username: string, password: string }) {
      const api = useApi()
      this.loading = true
      this.error = ''

      try {
        const { data } = await api.post<AuthResponse>('/accounts/login/', payload)
        this.persist(data.token)
        this.user = data.user
      } catch (error: any) {
        this.error = error.response?.data?.non_field_errors?.[0] || 'Could not sign in.'
        throw error
      } finally {
        this.loading = false
      }
    },

    async register(payload: {
      username: string
      email: string
      password: string
      household_name: string
    }) {
      const api = useApi()
      this.loading = true
      this.error = ''

      try {
        const { data } = await api.post<AuthResponse>('/accounts/register/', payload)
        this.persist(data.token)
        this.user = data.user
      } catch (error: any) {
        const data = error.response?.data
        this.error = data?.username?.[0] || data?.password?.[0] || 'Could not create your account.'
        throw error
      } finally {
        this.loading = false
      }
    },

    async logout() {
      const api = useApi()

      try {
        await api.post('/accounts/logout/')
      } finally {
        this.clear()
        await navigateTo('/login')
      }
    },
  },
})
