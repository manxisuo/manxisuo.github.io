<template>
  <div>
    <h1>
      <span class="post-time">{{time}}</span>
      <h2 class="post-link">
        <a :href="`#/post/${number}`">{{title}}</a>
        <el-tag type="info" class="post-comment">{{commentCount}}</el-tag>
      </h2>
    </h1>
  </div>
</template>

<script>
export default {
  name: 'post',
  props: ['title', 'number', 'time', 'commentCount']
}
</script>

<style scoped>
.post-time {
  color: #828282;
  font-size: 14px;
  font-weight: normal;
}

.post-link {
  line-height: 30px;
  margin: 0 0 10px 0;
}

.post-link * {
  vertical-align: middle;
}

.post-link a {
  color: #2a7ae2;
  font-size: 24px;
  font-weight: normal;
  text-decoration: none;
}

.post-link a:hover {
  color: #42b983;
  text-decoration: underline;
}

.post-comment {
  font-size: 15px;
  margin-left: 5px;
}
</style>
