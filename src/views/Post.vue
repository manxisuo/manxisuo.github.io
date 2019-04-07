<template>
  <div>
    <div>
      <PostContent
        :title="post.title"
        :content="post.content"
        :tags="post.tags" />
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
import PostContent from '@/components/PostContent.vue'
import Comment from '@/components/Comment.vue'
import axios from 'axios'
import util from '@/util.js'

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
      comments: []
    }
  },
  mounted() {
    const post_number = this.$route.params.post_number || 1 // 1是about页面的ID
    const url = `https://api.github.com/repos/manxisuo/blog/issues/${post_number}`
    axios(url).then(r => {
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
    })

    
    const url2 = `https://api.github.com/repos/manxisuo/blog/issues/${post_number}/comments`
    axios(url2).then(r => {
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
    })    
  }
}
</script>

<style scoped>

</style>
