<template>
  <div>
    <h3>Welcome to Scenario 3.</h3>
    <p>{{welcome_msg}}</p>
  </div>
</template>

<script>
import firebase from 'firebase'

export default {
  computed: {
    welcome_msg: function () {
      if (firebase.auth().currentUser) {
        return 'Your unique randomized ID is: ' + firebase.auth().currentUser.uid
      } else {
        console.log(firebase.auth().currentUser)
        return 'Please authenticate yourself before using this App'
      }
    }
  }
}
</script>
