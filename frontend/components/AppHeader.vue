<script setup lang="ts">
const auth = useAuthStore()
const route = useRoute()

const initials = computed(() => auth.user?.username?.slice(0, 2).toUpperCase() || 'SF')

const navItems = [
  {
    to: '/dashboard',
    label: 'Dashboard',
    icon: 'pi pi-chart-line',
  },
  {
    to: '/expenses',
    label: 'Expenses',
    icon: 'pi pi-wallet',
  },
  {
    to: '/receipts',
    label: 'Receipts',
    icon: 'pi pi-receipt',
  },
]
</script>

<template>
  <header class="app-header">
    <NuxtLink
      to="/dashboard"
      class="brand"
    >
      <span class="brand-mark">SF</span>
      <span>
        <span class="brand-title">Smart Finance AI</span>
        <span class="brand-subtitle">{{ auth.user?.households?.[0]?.name || 'Expense workspace' }}</span>
      </span>
    </NuxtLink>

    <nav
      class="nav-actions"
      aria-label="Primary navigation"
    >
      <NuxtLink
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        class="nav-link"
        :class="{
          'is-active': route.path === item.to,
        }"
      >
        <i :class="item.icon" />
        <span>{{ item.label }}</span>
      </NuxtLink>
    </nav>

    <div class="account-actions">
      <div class="user-chip">
        <Avatar
          :label="initials"
          shape="circle"
        />
        <span>
          <strong>{{ auth.user?.username }}</strong>
          <small>{{ auth.user?.email || 'authenticated user' }}</small>
        </span>
      </div>

      <Avatar
        class="mobile-avatar"
        :label="initials"
        shape="circle"
      />
      <Button
        aria-label="Sign out"
        icon="pi pi-sign-out"
        severity="secondary"
        text
        rounded
        @click="auth.logout"
      />
    </div>
  </header>
</template>
