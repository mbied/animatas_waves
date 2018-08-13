<template>
  <div>
    <div class="StateDisplay">
      <h3>Current State</h3>
        <div class="graph">
        <WaveCard ref="Wave1" :x="x_labels" :options="wave1_options" :y="wave1"></WaveCard>
      </div>
      <div id="WaveSum" class="graph">
        <WaveCard ref="SummedWaves" :x="x_labels" :y="SummedWave" :options="SummedWave_options"></WaveCard>
      </div>
      <div class="graph">
        <WaveCard ref="Wave2" :x="x_labels" :options="wave2_options" :y="wave2"></WaveCard>
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
import linspace from 'linspace'
import WaveCard from './WaveCard'

export default {
  components: {
    WaveCard
  },
  data () {
    return {
      time: linspace(0, 2 * Math.PI, 20),
      wave1_options: {
        previous: true
      },
      wave2_options: {
        previous: true
      },
      game_state: {
        wave1: {
          amplitude: 1,
          frequency: 1
        },
        wave2: {
          amplitude: 1,
          frequency: 1
        },
        target: {
          amplitude: 1,
          frequency: 1
        }
      }
    }
  },
  methods: {
    updateAmplitude (wave, value) {
      var self = this
      var guidanceData = {}
      guidanceData[wave] = {amplitude: value}
      axios.get('/api/feedback',
        {
          params: {
            feedback: 0,
            guidance: guidanceData
          }
        })
        .then(function (response) {
          var data = response.data
          self.game_state.wave1 = data.wave1
          self.game_state.wave2 = data.wave2
        })
    },
    updateFrequency (wave, value) {
      var self = this
      var guidanceData = {}
      guidanceData[wave] = {frequency: value}
      axios.get('/api/feedback',
        {
          params: {
            feedback: 0,
            guidance: guidanceData
          }
        })
        .then(function (response) {
          var data = response.data
          self.game_state.wave1 = data.wave1
          self.game_state.wave2 = data.wave2
        })
    },
    administerFeedback (value) {
      var self = this
      axios.get('/api/feedback',
        {
          params: {
            feedback: value
          }
        })
        .then(function (response) {
          var data = response.data
          self.game_state.wave1 = data.wave1
          self.game_state.wave2 = data.wave2
        })
    }
  },
  computed: {
    wave1: function () {
      return this.time.map(x => this.game_state.wave1.amplitude * Math.sin(this.game_state.wave1.frequency * x))
    },
    wave2: function () {
      return this.time.map(x => this.game_state.wave2.amplitude * Math.sin(this.game_state.wave2.frequency * x))
    },
    SummedWave: function () {
      return this.time.map(x => this.game_state.wave1.amplitude * Math.sin(this.game_state.wave1.frequency * x) +
                                     this.game_state.wave2.amplitude * Math.sin(this.game_state.wave2.frequency * x))
    },
    x_labels: function () {
      return this.time.map(x => Math.round(x * 100) / 100)
    },
    SummedWave_options: function () {
      return {
        target: this.time.map(x => this.game_state.target.amplitude * Math.sin(this.game_state.target.frequency * x))
      }
    }
  }
}
</script>

<style>
.StateDisplay {
  display: table-cell;
}

.graph {
  display: inline-block;
  vertical-align: bottom;
  width: 1;
  max-width: 30%;
}
#WaveSum {
  max-width: 40%;
}
</style>
