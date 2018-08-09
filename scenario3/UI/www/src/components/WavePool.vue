<template>
  <ul class="list">
    <slot />
  </ul>
</template>

<script>
// eslint-disable-next-line
import { ContainerMixin, ElementMixin } from 'vue-slicksort'

export default {
  props: ['item'],
  mixins: [ContainerMixin]
}
</script>
