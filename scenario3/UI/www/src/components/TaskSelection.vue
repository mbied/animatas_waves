<template>
  <div class="root">
    <router-link to="/Exercise" tag="button">Go To Exercise</router-link>
    <draggable id="wave1" class="wave" v-model="wave1" :options="{group:'people'}" @start="drag=true" @end="drag=false" :move="this.check_movement">
      <div v-for="element in wave1" :key="element.id">{{element.name}}</div>
    </draggable>
    <hr />
    <draggable id="wave2" class="wave" v-model="wave2" :options="{group:'people'}" @start="drag=true" @end="drag=false" :move="this.check_movement">
      <div v-for="element in wave2" :key="element.id">{{element.name}}</div>
    </draggable>
    <hr />
      <draggable v-model="myArray" :options="{group:'people'}" @start="drag=true" @end="drag=false" :move="this.check_movement">
        <div v-for="element in myArray" :key="element.id">
          <WaveCard></WaveCard>
        </div>
      </draggable>
  </div>
</template>

<script>
import draggable from 'vuedraggable'
import WaveCard from './WaveCard'

export default {
  name: 'TaskSelection',
  components: {
    draggable,
    WaveCard
  },
  data () {
    return {
      wave1: [],
      wave2: [],
      myArray: [
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
            frequency: 1
          }
        },
        {
          key: 3,
          data: {
            amplitude: 1,
            frequency: 1
          }
        },
        {
          key: 4,
          data: {
            amplitude: 1,
            frequency: 1
          }
        },
        {
          key: 5,
          data: {
            amplitude: 1,
            frequency: 1
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
    }
  }
}
</script>

<style scoped>
  .wave {
    min-height: 50px;
  }
</style>
