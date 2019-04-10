<template>
  <div>
    <div>
      <PostContent
        :title="post.title"
        :content="post.content"
        :tags="post.tags" />
      <el-alert v-if="errored" title="文章不存在" type="info" />
    </div>
    <div>
      <h2 v-if="comments.length">评论：</h2>
      <Comment v-for="comment in comments"
        :key="comment.id"
        v-bind="comment" />
    </div>
    <p>
      <a v-if="post.url" :href="post.url">&gt;&gt; 点击此处发表评论...</a>
    </p>
  </div>
</template>

<script>
import axios from 'axios'
import {REPO, ABOUT_NUMBER, API_PREFIX} from '@/config.js'
import util from '@/util.js'
import PostContent from '@/components/PostContent.vue'
import Comment from '@/components/Comment.vue'

export default {
  name: 'post',
  components: {PostContent, Comment},
  data () {
    return {
      post: {
        url: '',
        title: '',
        content: '',
        tags: []
      },
      errored: false,
      comments: []
    }
  },
  mounted() {
    const post_number = parseInt(this.$route.params.post_number) || ABOUT_NUMBER
    const p_url = `${API_PREFIX}/repos/${REPO}/issues/${post_number}`
    axios(p_url).then(r => {
      const item = r.data
      this.post = {
        id: item.id,
        title: item.title,
        url: item.html_url,
        time: util.convertTime(item.created_at),
        commentCount: item.comments,
        content: item.body,
        tags: item.labels
      }
    }).catch(e => {
      this.errored = true
    })
    
    const c_url = `${API_PREFIX}/repos/${REPO}/issues/${post_number}/comments`
    axios(c_url).then(r => {
      const item = r.data
      this.comments = r.data.map(item => ({
        id: item.id,
        user: item.user.login,
        avatar_url: item.user.avatar_url,
        time: util.convertTime(item.created_at),
        commentCount: item.comments,
        content: item.body,
        url: item.html_url
      }))
    }).catch(e => {})
  }
}
</script>

<style scoped>
</style>
