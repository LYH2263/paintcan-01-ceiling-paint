<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
const s = ref({})
const msg = ref('')
const load = async () => { s.value = await getJSON('/api/settings') }
onMounted(load)
const save = async () => {
  msg.value = ''
  try {
    s.value = await postJSON('/api/settings', {
      coverage: +s.value.coverage, coats: +s.value.coats,
      ceiling_coverage: +s.value.ceiling_coverage, ceiling_coats: +s.value.ceiling_coats,
    })
    msg.value = '已保存'
  } catch (e) { msg.value = '保存失败：' + e.message }
}
</script>
<template><div class="page"><h1>遮盖力参数</h1>
<table>
  <tr><th></th><th>涂布率 m²/L</th><th>默认遍数</th></tr>
  <tr><td>墙面</td><td><input v-model="s.coverage" /></td><td><input v-model="s.coats" /></td></tr>
  <tr><td>天花</td><td><input v-model="s.ceiling_coverage" /></td><td><input v-model="s.ceiling_coats" /></td></tr>
</table>
<button @click="save">保存</button>
<span v-if="msg" style="margin-left:1rem">{{ msg }}</span>
<p class="hint">修改默认值只影响之后的估算，已写入的历史记录钉选数不会改变。</p>
</div></template>
