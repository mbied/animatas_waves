<template>
  <div class="md-medium-size-25 md-small-size-100 md-gutter md-elevation-2">
    <h4>{{title}}</h4>
    <div class="md-layout">
      <div class="md-layout-item md-size-80">Amplitude</div>
      <div class="md-layout-item md-layout">
        <md-button class="md-layout-item md-size-100 md-icon-button md-raised" :disabled="value===title.concat(' - 1')" v-on:click="foo(1)">
          <i class="material-icons">keyboard_arrow_up</i>
        </md-button>
        <md-button class="md-layout-item md-size-100 md-icon-button md-raised" :disabled="value===title.concat(' - 2')" v-on:click="foo(2)">
          <i class="material-icons">keyboard_arrow_down</i>
        </md-button>
      </div>
    </div>
    <div class="md-layout">
      <div class="md-layout-item md-size-80">Frequency</div>
      <div class="md-layout-item md-layout">
        <md-button class="md-layout-item md-size-100 md-icon-button md-raised" :disabled="value===title.concat(' - 3')" v-on:click="foo(3)">
          <i class="material-icons">keyboard_arrow_up</i>
        </md-button>
        <md-button class="md-layout-item md-size-100 md-icon-button md-raised" :disabled="value===title.concat(' - 4')" v-on:click="foo(4)">
          <i class="material-icons">keyboard_arrow_down</i>
        </md-button>
      </div>
    </div>
  </div>
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
