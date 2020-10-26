<template>
  <div>
    <div class="college-pos">
      <choose-college/>
      <search-info/>
    </div>
    <hr>
    <room-card/>
  </div>
</template>
<script>
import ChooseCollege from './ChooseCollege'
import SearchInfo from './SearchInfo'
import RoomCard from './RoomCard'
export default {
  data() {
    return {}
  },
  methods: {},
  components: {
    ChooseCollege,
    SearchInfo,
    RoomCard
  }
}
</script>

<style scoped>
.college-pos {
  padding: 10px 20px;
}
</style>
