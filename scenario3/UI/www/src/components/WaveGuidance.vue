<template>
  <md-content class="md-layout md-small-size-100 md-gutter md-elevation-1">
    <h3 class="md-layout-item md-size-100">{{title}}</h3>
    <div class="md-layout-item md-layout md-elevation-1">
      <div class="md-layout-item"><h4>Amplitude</h4></div>
      <div class="md-layout-item md-layout">
        <div class='md-layout-item md-size-100'>
          <md-button class="md-icon-button md-raised" :disabled="value===title.concat(' - 1')" v-on:click="foo(1)">
            <i class="material-icons">keyboard_arrow_up</i>
          </md-button>
        </div>
        <div class='md-layout-item md-size-100'>
          <md-button class="md-icon-button md-raised" :disabled="value===title.concat(' - 2')" v-on:click="foo(2)">
            <i class="material-icons">keyboard_arrow_down</i>
          </md-button>
        </div>
      </div>
    </div>
    <div class="md-layout-item md-layout md-elevation-1">
      <div class="md-layout-item"><h4>Frequency</h4></div>
      <div class="md-layout-item md-layout">
        <div class="md-layout-item md-size-100">
          <md-button class="md-icon-button md-raised" :disabled="value===title.concat(' - 3')" v-on:click="foo(3)">
            <i class="material-icons">keyboard_arrow_up</i>
          </md-button>
        </div>
        <div class='md-layout-item md-size-100'>
          <md-button class="md-icon-button md-raised" :disabled="value===title.concat(' - 4')" v-on:click="foo(4)">
            <i class="material-icons">keyboard_arrow_down</i>
          </md-button>
        </div>
      </div>
    </div>
  </md-content>
</template>

<script>
export default {
  props: ['title', 'value'],
  methods: {
    foo (selected) {
      this.$emit('input', this.title.concat(' - ', selected.toString()))
    }
  }
}
</script>
