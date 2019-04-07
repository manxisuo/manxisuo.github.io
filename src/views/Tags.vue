<template>
  <div>
    <el-tag v-for="tag in tags"
      :key="tag.id" :type="curTag === tag.name ? '' : 'success'"
      @click="handleTagClick(tag.name)"
      class="gh-tag">{{tag.name}}</el-tag>
    <PostMeta
      v-for="post in posts"
      :key="post.id"
      v-bind="post" />
  </div>
</template>

<script>
import PostMeta from '@/components/PostMeta.vue'
import axios from 'axios'
import util from '@/util.js'

export default {
  components: {
    PostMeta
  },
  data () {
    return {
      curTag: '',
      tags: [],
      posts: []
    }
  },
  mounted () {
    const url = 'https://api.github.com/repos/manxisuo/blog/labels'
    axios(url).then(r => {
      this.tags = r.data.map(item => ({
        id: item.id,
        name: item.name,
        color: item.color
      }))
    })
  },
  methods: {
    handleTagClick (tagName) {
      this.curTag = tagName

      const url = `https://api.github.com/repos/manxisuo/blog/issues?labels=${tagName}`
      axios(url).then(r => {
        this.posts = r.data.map(item => ({
          id: item.id,
          number: item.number,
          title: item.title,
          url: item.url,
          time: util.convertTime(item.created_at),
          commentCount: item.comments
        }))
      })
    }
  }
}
</script>

<style scoped>
.gh-tag {
  margin: 3px;
  cursor: pointer;
}
</style>
