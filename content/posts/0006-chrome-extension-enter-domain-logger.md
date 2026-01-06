---
title: "Chrome扩展：输入域记录器"
date: 2013-11-10
draft: false
tags:
  - "Chrome"
  - "浏览器扩展"
  - "前端"
---

<!--
<link rel="chrome-webstore-item" href="https://chrome.google.com/webstore/detail/endkfhomobijnknngmdfcooaafdmfbfj" />
-->

记录下网页中的文本框、下拉框、单选框、复选框等输入组件的值，将来可以随时重新填写。

<!-- more -->

# 说明

+ 记录网站的用户名和密码，下次登录时不用再重新输入。
+ 记录表单中的数据，以后可以瞬间填充。

# 截图

![input-recorder](https://cloud.githubusercontent.com/assets/3950285/22852644/33e5a0ce-f07b-11e6-9561-aafb9d67046e.png)

# 链接

<https://chrome.google.com/webstore/detail/endkfhomobijnknngmdfcooaafdmfbfj>

<!--
<button onclick="install()" id="install-button">点击安装</button>
-->

<!--
<script type="text/javascript">
	var url = 'https://chrome.google.com/webstore/detail/endkfhomobijnknngmdfcooaafdmfbfj';
	$('head').append('<link rel="chrome-webstore-item" href="' + url + '" />');
	function install() {
		chrome.webstore.install(url, function() {
			// alert('安装成功');
		}, function(msg) {
			// alert('安装失败');
			alert(msg);
		});
	}

	$(function() {
		if (chrome.app.isInstalled) {
		  document.getElementById('install-button').style.display = 'none';
		}
	});
</script>
-->
