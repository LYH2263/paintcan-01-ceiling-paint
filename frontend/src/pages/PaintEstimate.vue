<script setup>
import { ref } from 'vue'
import { postJSON } from '../api'
const room_id = ref(1)
const ceiling_enabled = ref(false)
const ceiling_coverage = ref(null)
const ceiling_coats = ref(null)
const out = ref(null)
const err = ref('')
const run = async () => {
  err.value = ''
  const body = { room_id: room_id.value, persist: true, ceiling_enabled: ceiling_enabled.value }
  if (ceiling_enabled.value) {
    if (ceiling_coverage.value) body.ceiling_coverage = ceiling_coverage.value
    if (ceiling_coats.value) body.ceiling_coats = ceiling_coats.value
  }
  try { out.value = await postJSON('/api/estimate', body) } catch (e) { out.value = null; err.value = e.message }
}
</script>
<template><div class="page"><h1>估漆工作台</h1>
<label>房间ID <input v-model.number="room_id" /></label>
<label><input type="checkbox" v-model="ceiling_enabled" /> 计算天花漆</label>
<template v-if="ceiling_enabled">
  <label>天花涂布率(m²/L) <input v-model.number="ceiling_coverage" placeholder="默认" /></label>
  <label>天花遍数 <input v-model.number="ceiling_coats" placeholder="默认" /></label>
</template>
<button @click="run">估算</button>
<p v-if="err" class="err">{{ err }}</p>
<table v-if="out">
  <tr><th></th><th>面积 m²</th><th>升数 L</th><th>遍数</th></tr>
  <tr><td>墙面</td><td>{{ out.net_m2 }}</td><td>{{ out.liters }}</td><td>{{ out.coats }}</td></tr>
  <tr v-if="out.ceiling_enabled"><td>天花</td><td>{{ out.ceiling_m2 }}</td><td>{{ out.ceiling_liters }}</td><td>{{ out.ceiling_coats }}</td></tr>
</table>
</div></template>
