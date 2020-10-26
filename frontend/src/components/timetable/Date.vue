<template>
  <div v-bind:style="{height:dateInfo.interval+'px'}" class="date">{{dateInfo.time}}</div>
</template>

<script>
export default {
  props: {
    dateInfo: {
      interval: Number,
      time: String,
      isColor: Boolean
    }
  },
  name: 'date',
  data() {
    return {}
  }
}
</script>

<style scoped>
.date {
  border: none;
  font-size: 14px;
}
</style>
