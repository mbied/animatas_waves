<template>
  <div>
    <h2>Choose the Exercise</h2>
    <div class="md-elevation-2">
      <div class='md-layout'>
        <div class="md-layout-item md-large-size-25 md-medium-size-33 md-small-size-50 md-xsmall-size-100">
          <md-card>
            <md-card-header><h3>Wave 1</h3></md-card-header>
            <draggable id="wave1" class="wave md-layout" v-model="wave1" :options="{group:'waves'}" @start="drag=true" @end="drag=false" :move="this.check_movement">
              <WavePlot v-if="wave1.length > 0" :key="wave1[0].key" :y="wave1[0].data"></WavePlot>
            </draggable>
          </md-card>
        </div>

        <div class="md-layout-item md-large-size-25 md-medium-size-33 md-small-size-50 md-xsmall-size-100">
          <md-card>
            <md-card-header><h3>Wave 2</h3></md-card-header>
            <draggable id="wave2" class="wave md-layout" v-model="wave2" :options="{group:'waves'}" @start="drag=true" @end="drag=false" :move="this.check_movement">
              <WavePlot v-if="wave2.length > 0" :key="wave2[0].key" :y="wave2[0].data"></WavePlot>
            </draggable>
          </md-card>
        </div>
      </div>
      <md-button class="md-raised md-primary" v-on:click="create_exercise">Create</md-button>
    </div>
    <div>
      <p>Drag'n'Drop waves from here into the two slots above.</p>
      <draggable class="md-layout" v-model="BaseWaves" :options="{group:'waves'}" @start="drag=true" @end="drag=false" :move="this.check_movement">
        <div class="md-layout-item md-large-size-25 md-medium-size-33 md-small-size-50 md-xsmall-size-100" v-for="element in BaseWaves" :key="element.id">
          <WaveCard class="BaseWave" :y="element.data"></WaveCard>
        </div>
      </draggable>
    </div>
  </div>
</template>

<script>
import firebase from 'firebase'
import draggable from 'vuedraggable'
import WaveCard from './WaveCard'
import WavePlot from './WavePlot'

// var database = firebase.FirebaseDatabase.getInstance()
// var ref = database.getReference('server/saving-data/fireblog')


export default {
  name: 'TaskSelection',
  components: {
    draggable,
    WaveCard,
    WavePlot
  },
  data () {
    return {
      uid: '',
      wave1: [],
      wave2: [],
      BaseWaves: [
        {
          key: 1,
          data: {
            amplitude: 1,
            frequency: 1
          }
        },
        {
          key: 2,
          data: {
            amplitude: 1,
            frequency: 2
          }
        },
        {
          key: 3,
          data: {
            amplitude: 1,
            frequency: 3
          }
        },
        {
          key: 4,
          data: {
            amplitude: 1,
            frequency: 4
          }
        },
        {
          key: 5,
          data: {
            amplitude: 1,
            frequency: 5
          }
        },
        {
          key: 6,
          data: {
            amplitude: 1,
            frequency: 6
          }
        }
      ]
    }
  },
  methods: {
    check_movement: function (event, originalEvent) {
      if (event.to.id === 'wave1' && this.wave1.length > 0) {
        return false
      } else if (event.to.id === 'wave2' && this.wave2.length > 0) {
        return false
      } else {
        return true
      }
    },
    create_exercise: function (event) {
      this.$router.push('/Exercise')
    }
  },
  created () {
    var self = this
    function OnAuth (user) {
      if (user) {
        self.uid = user.uid
      }
    }
    firebase.auth().onAuthStateChanged(OnAuth)

    var data = firebase.database().ref('test')
    data.set('foo', 'bar')
    //var ref = database.getReference('server/saving-data/fireblog')
  }
}
</script>

<style scoped>
  .wave {
    min-height: 300px;
  }
  .BaseWave {
  }
</style>
