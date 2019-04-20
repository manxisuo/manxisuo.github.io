<template>
  <div>
    <template v-if="posts">
      <template v-if="posts.length > 0">
        <PostMeta v-for="post in posts" :key="post.id" v-bind="post" />
        <el-pagination v-if="!isSearchMode"
          layout="prev, pager, next" background
          @current-change="changePage"
          :current-page="page" :page-size="pageSize" :total="total"
          class="gh-pagination"></el-pagination>
      </template>
      <el-alert v-else title="不存在匹配的文章" type="info" />
    </template>
  </div>
</template>

<script>
import axios from 'axios'
import {AUTHOR, REPO, API_PREFIX, PAGE_SIZE} from '@/config.js'
import util from '@/util.js'
import PostMeta from '@/components/PostMeta.vue'

export default {
  name: 'home',
  components: {
    PostMeta
  },
  data () {
    return {
      isSearchMode: 'false',
      posts: null,
      pageSize: PAGE_SIZE,
      page: 1,
      total: 0
    }
  },
  mounted() {
    this.page = parseInt(this.$route.query.page) || 1
    this.load()
  },
  methods: {
    load() {
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

      const keyword = this.$route.query.keyword
      if (keyword) {
        this.isSearchMode = true
        this.doSearch(keyword, fn)
      }
      else {
        this.isSearchMode = false
        this.doQueryAll(fn)
      }
    },
    doSearch (keyword, fn) {
      const url = `${API_PREFIX}/search/issues`
      axios.get(url, {
        params: {
          q: `${keyword} user:${AUTHOR} repo:${REPO} author:${AUTHOR} type:issue in:title,body`,
          per_page: PAGE_SIZE,
          page: this.page
        }
      }).then(resp => {
        //this.fetchTotal(resp.headers['link'])
        fn(resp.data.items)
      })
    },
    doQueryAll (fn) {
      const url = `${API_PREFIX}/repos/${REPO}/issues`
      axios(url, {
        params: {
          per_page: PAGE_SIZE,
          page: this.page
        }
      }).then(resp => {
        this.fetchTotal(resp.headers['link'])
        fn(resp.data)
      })
    },
    changePage (page) {
      this.$router.push({path: '', query: {page: page}})
    },
    fetchTotal (link) {
      let groups = link.match(/per_page=(\d+)&page=(\d+)>; rel="last"/)
      if (groups) {
        this.total = parseInt(groups[1]) * parseInt(groups[2])
      }
      else {
        groups = link.match(/per_page=(\d+)&page=(\d+)>; rel="prev"/)
        this.total = parseInt(groups[1]) * parseInt(groups[2]) + 1
      }
    }
  }
}
</script>

<style scoped>
.gh-pagination {
  text-align: center;
}
</style>
