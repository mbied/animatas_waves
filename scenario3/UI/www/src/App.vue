<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
import firebase from 'firebase'

// Initialize Firebase
var config = {
  apiKey: 'AIzaSyCZU_UM2tFdZAFzJZkCarA_jlnBraH5X8k',
  authDomain: 'animatas-scenario3.firebaseapp.com',
  databaseURL: 'https://animatas-scenario3.firebaseio.com',
  projectId: 'animatas-scenario3',
  storageBucket: 'animatas-scenario3.appspot.com',
  messagingSenderId: '1053462726800'
}

firebase.initializeApp(config)

firebase.auth().onAuthStateChanged(function (user) {
  if (user) {
    console.log('Hello, ' + user.uid)
  } else {
    firebase.auth().signInAnonymously().catch(function (error) {
      console.log(error)
    })
  }
})

export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
