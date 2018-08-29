<template>
  <div>
    <h1>Exercise</h1>
    <div class="StateDisplay">
      <div class="graph">
        <WaveCard ref="Wave1" title="Input Wave 1" :y="game_state.wave1" :hasHistory="true"></WaveCard>
      </div>
      <div id="WaveSum" class="graph">
        <WaveCard ref="SummedWaves" title="Combined Waves" :y="game_state.wave1" :y2="game_state.wave2" :target="target"></WaveCard>
      </div>
      <div class="graph">
        <WaveCard ref="Wave2" title="Input Wave 2" :y="game_state.wave2" :hasHistory="true"></WaveCard>
      </div>
    </div>
    <div class="md-layout md-elevation-2">
      <wave-guidance class="md-layout-item md-alignment-top-left" title="Wave 1" v-model="guidance_selected"></wave-guidance>
      <wave-guidance class="md-layout-item md-alignment-top-right" title="Wave 2" v-model="guidance_selected"></wave-guidance>

      <div id="Feedback" class="md-layout-item md-size-100">
        <md-button class="md-raised" v-on:click="administerFeedback(1)">Positive Feedback</md-button>
        <md-button class="md-raised" v-on:click="administerFeedback(0)">Neutral Feedback</md-button>
        <md-button class="md-raised" v-on:click="administerFeedback(-1)">Negative Feedback</md-button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import firebase from 'firebase'
import WaveCard from './WaveCard'
import WaveGuidance from './WaveGuidance'

export default {
  components: {
    WaveCard,
    WaveGuidance
  },
  data () {
    return {
      guidance_selected: '',
      uid: '',
      id_token: '',
      task_id: '',
      game_state: {
        wave1: {
          amplitude: 1,
          frequency: 1
        },
        wave2: {
          amplitude: 1,
          frequency: 1
        }
      },
      target: {
        wave1: {
          amplitude: 1,
          frequency: 1
        },
        wave2: {
          amplitude: 1,
          frequency: 1
        }
      }
    }
  },
  methods: {
    updateAmplitude (wave, value) {
      var guidanceData = {}
      guidanceData[wave] = {amplitude: value}
      axios.get('/api/feedback',
        {
          headers: {
            'Authorization': this.id_token,
            'Task': this.task_id
          },
          params: {
            feedback: 0,
            guidance: guidanceData
          }
        })
    },
    updateFrequency (wave, value) {
      var guidanceData = {}
      guidanceData[wave] = {frequency: value}
      axios.get('/api/feedback',
        {
          headers: {
            'Authorization': this.id_token,
            'Task': this.task_id
          },
          params: {
            feedback: 0,
            guidance: guidanceData
          }
        })
    },
    administerFeedback (value) {
      var guidanceData = {}
      switch (this.guidance_selected) {
        case 'Wave 1 - 1':
          guidanceData = {'wave1': {'amplitude': 1}}
          break
        case 'Wave 1 - 2':
          guidanceData = {'wave1': {'amplitude': -1}}
          break
        case 'Wave 1 - 3':
          guidanceData = {'wave1': {'frequency': 1}}
          break
        case 'Wave 1 - 4':
          guidanceData = {'wave1': {'frequency': -1}}
          break

        case 'Wave 2 - 1':
          guidanceData = {'wave2': {'amplitude': 1}}
          break
        case 'Wave 2 - 2':
          guidanceData = {'wave2': {'amplitude': -1}}
          break
        case 'Wave 2 - 3':
          guidanceData = {'wave2': {'frequency': 1}}
          break
        case 'Wave 2 - 4':
          guidanceData = {'wave2': {'frequency': -1}}
          break

        default:
          guidanceData = {}
      }
      this.guidance_selected = ''

      axios.get('/api/feedback',
        {
          headers: {
            'Authorization': this.id_token,
            'Task': this.task_id
          },
          params: {
            feedback: value,
            guidance: guidanceData
          }
        })
    }
  },
  computed: {
    user_storage: function () {
      return firebase.database().ref('user_data/' + this.uid)
    },
    task_data: function () {
      return this.user_storage.child(this.task_id)
    }
  },
  mounted () {
    var self = this

    function getGoal (snap) {
      self.target = snap.val()
    }

    function getWave (snap, wave) {
      var data = snap.val()
      self.game_state[wave].amplitude = data.amplitude
      self.game_state[wave].frequency = data.frequency
    }

    function OnAuth (user) {
      if (user) {
        self.uid = user.uid
        user.getIdToken().then(token => (self.id_token = token))

        let dataLocation = firebase.database().ref('user_data')
          .child(user.uid).child(self.task_id)
        dataLocation.child('target').once('value').then(getGoal)
        dataLocation.child('wave1').on('value', (snap) => getWave(snap, 'wave1'))
        dataLocation.child('wave2').on('value', (snap) => getWave(snap, 'wave2'))
      }
    }
    firebase.auth().onAuthStateChanged(OnAuth)
  },
  created () {
    this.task_id = this.$route.params.task_id
  }
}
</script>

<style>
.graph {
  display: inline-block;
  vertical-align: bottom;
  width: 25%;
}
#WaveSum {
  width: 40%;
}
</style>
