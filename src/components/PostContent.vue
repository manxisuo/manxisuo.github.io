<template>
  <div v-if="title" class="post-box">
    <h1 class="gh-title">{{title}}</h1>
    <template v-if="tags">
      <el-tag v-for="tag in tags"
        :key="tag.id" type="success"
        class="gh-tag">{{tag.name}}</el-tag>
    </template>
    <div v-html="hlContent"></div>
  </div>
</template>

<script>
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/idea.css'
import 'prismjs/themes/prism.css'

export default {
  name: 'post-content',
  components: {
  },
  props: ['title', 'content', 'tags'],
  data () {
    return {
    }
  },
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
  mounted () {
  },
  methods: {
  }
}
</script>

<style scoped>
.post-box {
  border: 1px solid #dcdfe6;
  margin: 10px 0;
  padding: 0 20px 10px 20px;
}

.gh-title {
  text-align: center;
  border-bottom: 2px dashed #dcdfe6;
  padding-bottom: 20px;
  margin-bottom: 0px;
}

.gh-tag {
  margin: 10px 0 10px 10px;
  float: right;
}
</style>
