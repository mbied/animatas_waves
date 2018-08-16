<template>
  <md-card>
    <md-card-header><h3>{{header}}</h3></md-card-header>
    <md-card-content>
      <WavePlot :y="y" :y2="y2" :target="target" :hasHistory="hasHistory"></WavePlot>
    </md-card-content>
  </md-card>
</template>

<script>
import WavePlot from './WavePlot'

export default {
  components: {
    WavePlot
  },
  props: ['header', 'y', 'y2', 'target', 'hasHistory']
}
</script>
