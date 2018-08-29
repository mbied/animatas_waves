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
    <hr />
    <div class="Feedback">
      <h3>Feedback</h3>
      <md-button class="md-raised" v-on:click="administerFeedback(1)">Positive Feedback</md-button>
      <md-button class="md-raised" v-on:click="administerFeedback(0)">Neutral Feedback</md-button>
      <md-button class="md-raised" v-on:click="administerFeedback(-1)">Negative Feedback</md-button>
    </div>
    <hr />
    <div class="Guidance">
      <h3>Guidance</h3>
      <md-table>
        <md-table-row>
          <md-table-head></md-table-head>
          <md-table-head>Wave1</md-table-head>
          <md-table-head>Wave2</md-table-head>
        </md-table-row>
        <md-table-row>
          <md-table-cell>Amplitude</md-table-cell>
          <md-table-cell>
            <div>
              <md-button class="md-icon-button md-raised" v-on:click="updateAmplitude('wave1', 1)">
                <i class="material-icons">keyboard_arrow_up</i>
              </md-button>
            </div>
            <div>
              <md-button class="md-icon-button md-raised" v-on:click="updateAmplitude('wave1', -1)">
                <i class="material-icons">keyboard_arrow_down</i>
              </md-button>
            </div>
          </md-table-cell>
          <md-table-cell>
            <div>
              <md-button class="md-icon-button md-raised" v-on:click="updateAmplitude('wave2', 1)">
                <i class="material-icons">keyboard_arrow_up</i>
              </md-button>
            </div>
            <div>
              <md-button class="md-icon-button md-raised" v-on:click="updateAmplitude('wave2', -1)">
                <i class="material-icons">keyboard_arrow_down</i>
              </md-button>
            </div>
          </md-table-cell>
        </md-table-row>
        <md-table-row>
          <md-table-cell>Frequency</md-table-cell>
          <md-table-cell>
            <div>
              <md-button class="md-icon-button md-raised" v-on:click="updateFrequency('wave1', 1)">
                <i class="material-icons">keyboard_arrow_up</i>
              </md-button>
            </div>
            <div>
              <md-button class="md-icon-button md-raised" v-on:click="updateFrequency('wave1', -1)">
                <i class="material-icons">keyboard_arrow_down</i>
              </md-button>
            </div>
          </md-table-cell>
          <md-table-cell>
            <div>
              <md-button class="md-icon-button md-raised" v-on:click="updateFrequency('wave2', 1)">
                <i class="material-icons">keyboard_arrow_up</i>
              </md-button>
            </div>
            <div>
              <md-button class="md-icon-button md-raised" v-on:click="updateFrequency('wave2', -1)">
                <i class="material-icons">keyboard_arrow_down</i>
              </md-button>
            </div>
          </md-table-cell>
        </md-table-row>
      </md-table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import firebase from 'firebase'
import WaveCard from './WaveCard'

export default {
  components: {
    WaveCard
  },
  data () {
    return {
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
      axios.get('/api/feedback',
        {
          headers: {
            'Authorization': this.id_token,
            'Task': this.task_id
          },
          params: {
            feedback: value
          }
        })
        .then(response => { console.log('test') })
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
