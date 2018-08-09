<template>
  <li class="list-item">{{item}}</li>
</template>

<script>
// eslint-disable-next-line
import { ContainerMixin, ElementMixin } from 'vue-slicksort'

export default {
  mixins: [ElementMixin],
  props: ['item']
}
</script>
