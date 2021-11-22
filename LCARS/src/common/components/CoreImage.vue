<template>
  <img :src="src"/>
</template>

<script>
export default {
  name: "core-image",
  props: {
    src: {
      default: '',
      type: String,
    }
  },
}
</script>

<style scoped>

</style>