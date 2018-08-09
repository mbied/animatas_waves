<template>
  <div class="root">
    <WavePool lockAxis="yx" axis="xy" v-model="items">
      <Wave v-for="(item, index) in items" :index="index" :key="index" :item="item"/>
    </WavePool>
    Some Random Text
    <WavePool axis="xy" v-model="items" style="min-height:20px;">
    </WavePool>
  </div>
</template>

<script>
import Wave from './Wave'
import WavePool from './WavePool'
// eslint-disable-next-line
import { ContainerMixin, ElementMixin } from 'vue-slicksort'

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
      ],
      items2: [
        'Item 19'
      ]
    }
  }
}
</script>
