import Avatar from 'primevue/avatar'
import Badge from 'primevue/badge'
import Button from 'primevue/button'
import Card from 'primevue/card'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import DatePicker from 'primevue/datepicker'
import Divider from 'primevue/divider'
import FileUpload from 'primevue/fileupload'
import InputNumber from 'primevue/inputnumber'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Password from 'primevue/password'
import ProgressSpinner from 'primevue/progressspinner'
import Tab from 'primevue/tab'
import TabList from 'primevue/tablist'
import TabPanel from 'primevue/tabpanel'
import TabPanels from 'primevue/tabpanels'
import Tabs from 'primevue/tabs'
import Tag from 'primevue/tag'

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.component('Avatar', Avatar)
  nuxtApp.vueApp.component('Badge', Badge)
  nuxtApp.vueApp.component('Button', Button)
  nuxtApp.vueApp.component('Card', Card)
  nuxtApp.vueApp.component('DataTable', DataTable)
  nuxtApp.vueApp.component('Column', Column)
  nuxtApp.vueApp.component('DatePicker', DatePicker)
  nuxtApp.vueApp.component('Divider', Divider)
  nuxtApp.vueApp.component('FileUpload', FileUpload)
  nuxtApp.vueApp.component('InputNumber', InputNumber)
  nuxtApp.vueApp.component('InputText', InputText)
  nuxtApp.vueApp.component('Message', Message)
  nuxtApp.vueApp.component('Password', Password)
  nuxtApp.vueApp.component('ProgressSpinner', ProgressSpinner)
  nuxtApp.vueApp.component('Tab', Tab)
  nuxtApp.vueApp.component('TabList', TabList)
  nuxtApp.vueApp.component('TabPanel', TabPanel)
  nuxtApp.vueApp.component('TabPanels', TabPanels)
  nuxtApp.vueApp.component('Tabs', Tabs)
  nuxtApp.vueApp.component('Tag', Tag)
})
