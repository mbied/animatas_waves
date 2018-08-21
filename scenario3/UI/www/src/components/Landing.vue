<template>
  <div>
    <h3>Welcome to Scenario 3.</h3>
    <p>{{welcome_msg}}</p>
    <div>
      <router-link :disabled="!allow_continue" to="/task-selection" tag="button">Select A Task</router-link>
    </div>
  </div>
</template>

<script>
import firebase from 'firebase'

export default {
  data: function () {
    return {
      uid: ''
    }
  },
  computed: {
    allow_continue: function () {
      if (this.uid) {
        return true
      }
      return false
    },
    welcome_msg: function () {
      if (this.uid) {
        return 'Your unique randomized ID is: ' + this.uid
      } else {
        return "We are trying to assign a random ID. If this text dosen't change within the next few seconds, please reload the page"
      }
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
  }
}
</script>
