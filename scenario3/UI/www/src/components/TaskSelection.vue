<template>
  <div class="root">
    <WavePool lockAxis="y" v-model="items">
      <Wave v-for="(item, index) in items" :index="index" :key="index" :item="item"/>
    </WavePool>
  </div>
</template>

<script>
import Wave from './Wave'
import WavePool from './WavePool'

import { ContainerMixin, ElementMixin } from 'vue-slicksort';

const SortableList = {
  mixins: [ContainerMixin],
  template: `
    <ul class="list">
      <slot />
    </ul>
  `
};

export default {
  name: 'TaskSelection',
  components: {
    Wave,
    WavePool
  },
  data () {
    return {
      items: [
        'Item 1',
        'Item 2',
        'Item 3',
        'Item 4',
        'Item 5',
        'Item 6',
        'Item 7',
        'Item 8'
      ]
    }
  }
}
</script>
