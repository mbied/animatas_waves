<template>
  <div>
    <button v-on:click="updateDataExample">Foo</button>
    <p>Exercis Screen</p>
    <WaveCard ref="wave" class="graph" :data="plot_data"></WaveCard>
  </div>
</template>

<script>
import WaveCard from './WaveCard'

export default {
  components: {
    WaveCard
  },
  data () {
    return {
      plot_data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        datasets: [
          {
            label: 'GitHub Commits',
            backgroundColor: '#f87979',
            data: [40, 20, 12, 39, 10, 40, 39, 80, 40, 20, 12, 11]
          }
        ]
      }
    }
  },
  methods: {
    updateDataExample () {
      this.plot_data.datasets[0].data[7] = (this.plot_data.datasets[0].data[7] - 1) % 50
      this.$refs.wave.update()
    }
  }
}

</script>

<style>
.graph {
  width: 10;
  height: 10px;
}
</style>
