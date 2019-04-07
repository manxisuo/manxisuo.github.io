<template>
  <div>
    <template v-if="posts">
      <template v-if="posts.length > 0">
        <PostMeta v-for="post in posts" :key="post.id" v-bind="post" />
      </template>
      <el-alert v-else title="不存在匹配的文章" type="info" />
    </template>
  </div>
</template>

<script>
import PostMeta from '@/components/PostMeta.vue'
import axios from 'axios'
import util from '@/util.js'

export default {
  name: 'home',
  components: {
    PostMeta
  },
  data () {
    return {
      posts: null
    }
  },
  mounted() {
    const fn = (items) => {
      this.posts = items.map(item => ({
        id: item.id,
        number: item.number,
        title: item.title,
        url: item.url,
        time: util.convertTime(item.created_at),
        commentCount: item.comments
      }))
    }

    const kw = this.$route.query.kw
    if (kw) {
      this.doSearch(kw, fn)
    }
    else {
      this.doQueryAll(fn)
    }
  },
  methods: {
    doSearch (kw, fn) {
      const url = `https://api.github.com/search/issues`
      axios.get(url, {
        params: {
          q: `${kw} user:manxisuo repo:manxisuo/blog author:manxisuo type:issue in:title,body`
        }
      }).then(resp => {
        fn(resp.data.items)
      })
    },
    doQueryAll (fn) {
      const url = 'https://api.github.com/repos/manxisuo/blog/issues'
      axios(url).then(resp => {
        fn(resp.data)
      })
    }
  }
}
</script>
