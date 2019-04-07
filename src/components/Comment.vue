<template>
  <div class="gh-comment-box">
    <div class="header">
      <img :src="avatar_url" class="avatar_img" />
      <a :href="url">{{user}}</a>
      <span> @ </span>
      <span class="post-time">{{time}}</span>
    </div>
    <div v-html="hlContent"></div>
  </div>
</template>

<script>
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/idea.css'
import 'prismjs/themes/prism.css'

export default {
  name: 'post',
  props: ['user', 'time', 'content', 'url', 'avatar_url'],
  computed: {
    hlContent () {
      const md = new MarkdownIt({
        html: true,
        linkify: true,
        typographer: true,
        highlight: function (str, lang) {
          if (lang && hljs.getLanguage(lang)) {
            try {
              return hljs.highlight(lang, str).value;
            } catch (__) {}
          }
          return ''; // use external default escaping
        }
      })
      return md.render(this.content)
    }
  },
}
</script>

<style scoped>
.header {
  vertical-align: middle;
}
.header > * {
  vertical-align: middle;
}
.avatar_img {
  width: 15px;
  margin-right: 5px;
}
.gh-comment-box {
  border: 1px solid #dcdfe6;
  margin: 10px 0;
  padding: 5px;
}
.post-time {
  color: #828282;
  font-size: 14px;
  font-weight: normal;
}
</style>
