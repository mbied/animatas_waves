import Vue from 'vue'
import Router from 'vue-router'
import Landing from '@/components/Landing'
import Exercise from '@/components/Exercise'
import TaskSelection from '@/components/TaskSelection'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Landing',
      component: Landing
    },
    {
      path: '/task-selection',
      name: 'Task Selection',
      component: TaskSelection
    },
    {
      path: '/exercise',
      name: 'Exercise',
      component: Exercise
    }
  ]
})
