import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Post from './views/Post.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/post/:post_number',
      name: 'post',
      component: Post
    },
    {
      path: '/projects',
      name: 'projects',
      component: () => import('./views/Projects.vue')
    },
    {
      path: '/tags',
      name: 'tags',
      component: () => import('./views/Tags.vue')
    },
    {
      path: '/search',
      name: 'search',
      component: Home
    },
    {
      path: '/about',
      name: 'about',
      component: Post
    }
  ]
})
