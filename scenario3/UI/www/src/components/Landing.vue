<template>
  <div>
    <h3>Welcome to Scenario 3.</h3>
    <p>{{welcome_msg}}</p>
    <div><button v-on:click="get_user_id()">Get Token</button><router-link :disabled="!allow_continue" to="/Exercise" tag="button">Go To Exercise</router-link></div>
  </div>
</template>

<script>
import firebase from 'firebase'

export default {
  data: function () {
    return {
      welcome_msg: 'Please authenticate yourself before using this App',
      uid: ''
    }
  },
  methods: {
    get_user_id: function (event) {
      if (firebase.auth().currentUser) {
        this.welcome_msg = 'Your unique randomized ID is: ' + firebase.auth().currentUser.uid
        this.uid = firebase.auth().currentUser.uid
      }
    }
  },
  computed: {
    allow_continue: function () {
      if (this.uid) {
        return true
      }
      return false
    }
  }
}
</script>
