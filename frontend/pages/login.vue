<script setup lang="ts">
const auth = useAuthStore()

const loginForm = reactive({
  username: '',
  password: '',
})

const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  household_name: '',
})

async function submitLogin() {
  await auth.login(loginForm)
  await navigateTo('/dashboard')
}

async function submitRegister() {
  await auth.register(registerForm)
  await navigateTo('/dashboard')
}

onMounted(() => {
  auth.hydrate()

  if (auth.isAuthenticated) {
    navigateTo('/dashboard')
  }
})
</script>

<template>
  <main class="auth-page">
    <section class="auth-panel">
      <div class="auth-panel__content">
        <p class="eyebrow">Smart Finance AI</p>
        <h1>Sign in, record expenses, and upload receipts.</h1>
        <p>
          After signing in, you can add an expense manually or upload a receipt.
          Both flows feed the same finance dashboard.
        </p>

        <div class="auth-steps">
          <div class="auth-step">
            <span>1</span>
            <strong>Create your account</strong>
            <p>A default household workspace is created for your expenses.</p>
          </div>
          <div class="auth-step">
            <span>2</span>
            <strong>Add expenses</strong>
            <p>Use the manual form for quick spending entries.</p>
          </div>
          <div class="auth-step">
            <span>3</span>
            <strong>Upload receipts</strong>
            <p>Send a PDF or image for background processing.</p>
          </div>
        </div>
      </div>
    </section>

    <div class="auth-form-wrap">
      <Card class="auth-card">
        <template #title>
          Access your account
        </template>

        <template #subtitle>
          Sign in first. Then you will land directly on the dashboard.
        </template>

        <template #content>
          <Tabs value="login">
            <TabList>
              <Tab value="login">Sign in</Tab>
              <Tab value="register">Create account</Tab>
            </TabList>

            <TabPanels>
              <TabPanel value="login">
                <form
                  class="form-stack"
                  @submit.prevent="submitLogin"
                >
                  <Message
                    v-if="auth.error"
                    severity="error"
                  >
                    {{ auth.error }}
                  </Message>

                  <div class="field">
                    <label for="login-username">Username</label>
                    <InputText
                      id="login-username"
                      v-model="loginForm.username"
                      autocomplete="username"
                      required
                    />
                  </div>

                  <div class="field">
                    <label for="login-password">Password</label>
                    <Password
                      id="login-password"
                      v-model="loginForm.password"
                      autocomplete="current-password"
                      :feedback="false"
                      toggle-mask
                      required
                    />
                  </div>

                  <Button
                    type="submit"
                    label="Open dashboard"
                    icon="pi pi-sign-in"
                    :loading="auth.loading"
                  />
                </form>
              </TabPanel>

              <TabPanel value="register">
                <form
                  class="form-stack"
                  @submit.prevent="submitRegister"
                >
                  <Message
                    v-if="auth.error"
                    severity="error"
                  >
                    {{ auth.error }}
                  </Message>

                  <div class="field">
                    <label for="register-username">Username</label>
                    <InputText
                      id="register-username"
                      v-model="registerForm.username"
                      autocomplete="username"
                      required
                    />
                  </div>

                  <div class="field">
                    <label for="register-email">Email</label>
                    <InputText
                      id="register-email"
                      v-model="registerForm.email"
                      type="email"
                      autocomplete="email"
                    />
                  </div>

                  <div class="field">
                    <label for="household-name">Household name</label>
                    <InputText
                      id="household-name"
                      v-model="registerForm.household_name"
                      placeholder="Example: Family home, Apartment, Studio"
                    />
                    <small class="tiny">This workspace groups your expenses and receipts.</small>
                  </div>

                  <div class="field">
                    <label for="register-password">Password</label>
                    <Password
                      id="register-password"
                      v-model="registerForm.password"
                      autocomplete="new-password"
                      toggle-mask
                      required
                    />
                  </div>

                  <Button
                    type="submit"
                    label="Create account and enter"
                    icon="pi pi-user-plus"
                    :loading="auth.loading"
                  />
                </form>
              </TabPanel>
            </TabPanels>
          </Tabs>
        </template>
      </Card>
    </div>
  </main>
</template>
