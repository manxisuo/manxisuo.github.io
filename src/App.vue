<template>
  <div>
    <el-row>
      <el-col :span="24">
        <div class="gh-header">
          <div class="gh-header-wrapper">
            <h2 class="gh-title">
              <img src="avatar.jpg" class="gh-avatar">
              <router-link to="/">{{title}}</router-link>
            </h2>
            <div id="nav">
              <router-link to="/">首页</router-link>
              <router-link to="/projects">项目</router-link>
              <router-link to="/tags">标签</router-link>
              <router-link to="/about">关于</router-link>
            </div>
            <div class="search-box">
              <el-input placeholder="搜索文章" v-model="kw" @keyup.enter.native="searchPosts">
                <el-button slot="append" icon="el-icon-search" @click="searchPosts"></el-button>
              </el-input>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="24">
        <div class="gh-body">
          <div class="gh-body-wrapper">
            <keep-alive>
              <router-view :key="routerKey" />
            </keep-alive>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from 'axios'
import {TITLE} from '@/config.js'

export default {
  data () {
    return {
      kw: '',
      title: TITLE
    }
  },
  computed: {
    routerKey () {
      // return this.$route.path
      return this.$route.path + '@' + Math.random()
    }
  },
  methods: {
    searchPosts () {
      this.$router.push({path: 'search', query: {kw: this.kw}})
    }
  }
}
</script>

<style>
body {
  margin-top: 0;
  font-family: consolas;
}

/* h1, h2, h3, h4, h5, h6 {
  margin: 0;
  padding: 0;
} */

pre {
  background-color: #dcdfe6;
  padding: 10px;
}

/* p:has(img) {
  text-align: center;
} */

img {
  border: 1px solid #dcdfe6;
  padding: 5px;
  border-radius: 5px;  
  max-width: 100%;
}
</style>

<style scoped>
#nav {
  line-height: 55px;
  float: right;
  vertical-align: middle;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
  margin-left: 20px;
  text-decoration: none;
  vertical-align: middle;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

.gh-header {
  border-bottom: 1px solid #dcdfe6;
  height: 55px;
}

.gh-header-wrapper {
  margin-left: auto;
  margin-right: auto;
  max-width: 880px;
}

.gh-title {
  margin: 0;
  line-height: 55px;
  color: #409eff;
  font-weight: normal;
  float: left;
}

.gh-title > * {
    vertical-align: middle;
}

.gh-title a {
  color: #409eff;
  cursor: pointer;
  text-decoration: none;
}

.gh-avatar {
    width: 31px;
    height: 31px;
    margin-right: 5px;
    vertical-align: middle;
    border-radius: 5px;
}

.gh-body-wrapper {
    max-width: 880px;
    margin: 15px auto 0 auto;
}

.search-box {
  line-height: 56px;
  float: right;
}
</style>
