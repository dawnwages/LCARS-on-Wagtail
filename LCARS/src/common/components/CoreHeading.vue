<template>
<span
    :class="{
        'h1' : hsize === 'h1',
        'h2' : hsize === 'h2',
        'h3' : hsize === 'h3',
        'h4' : hsize === 'h4',
        'h5' : hsize === 'h5',
        'h6' : hsize === 'h6',
      }">{{ text }}</span>
</template>

<script>
export default {
  name: "core-heading",
  props: {
    text: {
      default: '',
      type: String,
    },
    hsize: {
      default: 'h1',
      type: String,
    }
  },
}
</script>

<style scoped>
  .h1 {
    font-size: calc(var(--lcars-title-size) * 1.25);;
  }
  .h2 {
    font-size: calc(var(--lcars-title-size) * 1.15);;
  }
  .h3 {
    font-size: calc(var(--lcars-title-size) * 1.1);;
  }
  .h4 {
    font-size: calc(var(--lcars-title-size) * 1.05);;
  }
  .h5 {
    font-size: calc(var(--lcars-title-size) * 1);;
  }
  .h6 {
    font-size: calc(var(--lcars-title-size) * .95);;
  }

  h1, h2, h3, h4, h5, h6 {
  font-weight: 100;
  }
</style>