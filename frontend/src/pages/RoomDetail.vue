<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getJSON, postJSON } from '../api'
const route = useRoute()
const detail = ref(null)
const est = ref(null)
const ceiling_enabled = ref(false)
const load = async () => {
  detail.value = await getJSON(`/api/rooms/${route.params.id}`)
  est.value = await postJSON('/api/estimate', { room_id: +route.params.id, persist: false, ceiling_enabled: ceiling_enabled.value })
}
onMounted(load)
watch(() => route.params.id, load)
watch(ceiling_enabled, load)
</script>
<template><div class="page" v-if="detail"><h1>{{ detail.room.name }}</h1>
<label><input type="checkbox" v-model="ceiling_enabled" /> 计算天花漆</label>
<table>
  <tr><th></th><th>面积 m²</th><th>需漆 L</th></tr>
  <tr><td>墙面</td><td>{{ est?.net_m2 }}</td><td><span class="hero-num">{{ est?.liters }}</span></td></tr>
  <tr v-if="est?.ceiling_enabled"><td>天花</td><td>{{ est.ceiling_m2 }}</td><td><span class="hero-num">{{ est.ceiling_liters }}</span></td></tr>
</table>
<ul><li v-for="o in detail.openings" :key="o.id">{{ o.kind }} {{ o.w }}×{{ o.h }}</li></ul>
</div></template>
