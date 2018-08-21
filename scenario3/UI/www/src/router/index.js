import Vue from 'vue'
import Router from 'vue-router'
import firebase from 'firebase'
import Landing from '@/components/Landing'
import Exercise from '@/components/Exercise'
import TaskSelection from '@/components/TaskSelection'

Vue.use(Router)

let router = new Router({
  routes: [
    {
      path: '/',
      name: 'Landing',
      component: Landing
    },
    {
      path: '/task-selection',
      name: 'Task Selection',
      component: TaskSelection,
      auth: {
        auth: true
      }
    },
    {
      path: '/exercise/:task_id',
      name: 'Exercise',
      component: Exercise,
      meta: {
        auth: true
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.auth)) {
    firebase.auth().onAuthStateChanged(function (user) {
      if (!user) {
        console.log('Authenticated')
        next({
          path: '/'
        })
      } else {
        next()
      }
    })
  } else {
    next()
  }
})

export default router
