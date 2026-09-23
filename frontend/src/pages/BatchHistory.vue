<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
const qid = ref('')
const detail = ref(null)
const err = ref('')
onMounted(async () => { items.value = (await getJSON('/api/history')).items })
const fetchOne = async () => {
  err.value = ''; detail.value = null
  if (!qid.value) return
  try { detail.value = await getJSON(`/api/history/${qid.value}`) } catch (e) { err.value = e.message }
}
</script>
<template><div class="page"><h1>估算记录</h1>
<label>按编号查询 <input v-model="qid" @keyup.enter="fetchOne" /></label>
<button @click="fetchOne">取出</button>
<p v-if="err" class="err">{{ err }}</p>
<table v-if="detail">
  <tr><th>编号</th><th>房间</th><th>时间</th><th>天花开关</th><th>墙面升数 L</th><th>天花升数 L</th></tr>
  <tr>
    <td>#{{ detail.id }}</td><td>{{ detail.room_id }}</td><td>{{ detail.created_at }}</td>
    <td>{{ detail.ceiling_enabled ? '启用' : '关闭' }}</td>
    <td>{{ detail.wall_liters }}</td><td>{{ detail.ceiling_enabled ? detail.ceiling_liters : '—' }}</td>
  </tr>
</table>
<hr />
<table><tr v-for="h in items" :key="h.id"><td>#{{ h.id }}</td><td>{{ h.created_at }}</td></tr></table>
</div></template>
