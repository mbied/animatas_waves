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
      <md-button class="md-raised md-primary" :disabled="!allow_creation" v-on:click="create_exercise">Create</md-button>
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
      BaseWaves: [],
      foobar: 0,
      common_storage: firebase.database().ref('shared_data/')
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
      let key = this.user_storage.push().key
      let taskStorage = this.user_storage.child(key)

      taskStorage.child('wave1').set({amplitude: 1, frequency: 1})
      taskStorage.child('wave2').set({amplitude: 1, frequency: 10})

      taskStorage.child('target').child('wave1').set(this.wave1[0].data)
      taskStorage.child('target').child('wave2').set(this.wave2[0].data)

      this.$router.push({name: 'Exercise', params: {task_id: key}})
    }
  },
  computed: {
    user_storage: function () {
      return firebase.database().ref('user_data/' + this.uid)
    },
    allow_creation: function () {
      if (!this.uid) {
        return false
      }

      if (this.wave1.length !== 1) {
        return false
      }

      if (this.wave2.length !== 1) {
        return false
      }

      return true
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

    function OnBaseWaveReceived (snap) {
      let content = snap.val()
      for (let key in content) {
        self.BaseWaves.push({
          key: key,
          data: content[key]
        })
      }
    }
    var baseWaveLocation = this.common_storage.child('base_waves')
    baseWaveLocation.once('value').then(OnBaseWaveReceived)
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
