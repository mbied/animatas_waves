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
      <table>
        <tr>
          <th></th>
          <th>Wave1</th>
          <th>Wave2</th>
        </tr>
        <tr>
          <td rowspan=2>Amplitude</td>
          <td>
            <md-button class="md-icon-button md-raised" v-on:click="updateAmplitude('wave1', 1)">
              <i class="material-icons">keyboard_arrow_up</i>
            </md-button>
          </td>
          <td>
            <md-button class="md-icon-button md-raised" v-on:click="updateAmplitude('wave2', 1)">
              <i class="material-icons">keyboard_arrow_up</i>
            </md-button>
          </td>
        </tr>
        <tr>
          <td>
            <md-button class="md-icon-button md-raised" v-on:click="updateAmplitude('wave1', -1)">
              <i class="material-icons">keyboard_arrow_down</i>
            </md-button>
          </td>
          <td>
            <md-button class="md-icon-button md-raised" v-on:click="updateAmplitude('wave2', -1)">
              <i class="material-icons">keyboard_arrow_down</i>
            </md-button>
          </td>
        </tr>
        <hr />
        <tr>
          <td rowspan=2>Frequency</td>
          <td>
            <md-button class="md-icon-button md-raised" v-on:click="updateFrequency('wave1', 1)">
              <i class="material-icons">keyboard_arrow_up</i>
            </md-button>
          </td>
          <td>
            <md-button class="md-icon-button md-raised" v-on:click="updateFrequency('wave2', 1)">
              <i class="material-icons">keyboard_arrow_up</i>
            </md-button>
          </td>
        </tr>
        <tr>
          <td>
            <md-button class="md-icon-button md-raised" v-on:click="updateFrequency('wave1', -1)">
              <i class="material-icons">keyboard_arrow_down</i>
            </md-button>
          </td>
          <td>
            <md-button class="md-icon-button md-raised" v-on:click="updateFrequency('wave2', -1)">
              <i class="material-icons">keyboard_arrow_down</i>
            </md-button>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
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
      this.game_state[wave].amplitude += value
    },
    updateFrequency (wave, value) {
      this.game_state[wave].frequency += value
    },
    administerFeedback (value) {
      console.log('Feedback: ' + value.toString())
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
