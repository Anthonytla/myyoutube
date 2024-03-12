<template>
  <v-container>
    <div v-for="i in idx" :key="i" @click="onGoToSelect(i)">
      <v-btn>
        {{ i }}
      </v-btn>
    </div>
  </v-container>
</template>

<script>
export default {
  data() {
    var idx = [];
    console.log("cpn:", this.currentPage);
    for (var i = 1; i <= this.totalPages; i++) {
      idx.push(i);
    }
    return {
      idx: idx,
    };
  },
  props: ["currentPage", "totalPages", "onGoToSelect"],
};
</script>

<style lang="scss" scoped>
.container {
  display: flex;
}

.pagination {
  justify-content: flex-start;
  display: flex;
}

.item {
  justify-content: space-around;
  padding-left: 8px;
}
</style>