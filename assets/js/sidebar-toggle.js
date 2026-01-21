// 侧边栏收起/展开功能
(function() {
    'use strict';

    // 左侧边栏切换
    const leftSidebarToggle = document.getElementById('toggle-left-sidebar');
    const leftSidebar = document.querySelector('.left-sidebar');
    
    // 右侧边栏切换
    const rightSidebarToggle = document.getElementById('toggle-right-sidebar');
    const rightSidebar = document.querySelector('.right-sidebar');

    // 从 localStorage 读取状态
    const leftSidebarCollapsed = localStorage.getItem('leftSidebarCollapsed') === 'true';
    const rightSidebarCollapsed = localStorage.getItem('rightSidebarCollapsed') === 'true';

    // 初始化状态
    if (leftSidebarCollapsed && leftSidebar) {
        document.body.classList.add('left-sidebar-collapsed');
    }
    if (rightSidebarCollapsed && rightSidebar) {
        document.body.classList.add('right-sidebar-collapsed');
    }

    // 左侧边栏切换
    if (leftSidebarToggle && leftSidebar) {
        leftSidebarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const isCollapsed = document.body.classList.toggle('left-sidebar-collapsed');
            localStorage.setItem('leftSidebarCollapsed', isCollapsed.toString());
        });
    }

    // 右侧边栏切换
    if (rightSidebarToggle && rightSidebar) {
        rightSidebarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const isCollapsed = document.body.classList.toggle('right-sidebar-collapsed');
            localStorage.setItem('rightSidebarCollapsed', isCollapsed.toString());
        });
    }
})();
