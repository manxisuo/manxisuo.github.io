/* Sidebar preferences apply on desktop; mobile navigation stays accessible. */
(function () {
    'use strict';
    function readPreference(key) {
        try { return localStorage.getItem(key) === 'true'; } catch (_) { return false; }
    }
    function writePreference(key, value) {
        try { localStorage.setItem(key, String(value)); } catch (_) { /* Private browsing. */ }
    }
    ['left', 'right'].forEach(function (side) {
        const button = document.getElementById('toggle-' + side + '-sidebar');
        const sidebar = document.querySelector('.' + side + '-sidebar');
        if (!button || !sidebar) return;
        const key = side + 'SidebarCollapsed';
        const className = side + '-sidebar-collapsed';
        function sync(collapsed) {
            document.body.classList.toggle(className, collapsed);
            button.setAttribute('aria-expanded', String(!collapsed));
        }
        sync(readPreference(key));
        button.addEventListener('click', function () {
            const collapsed = !document.body.classList.contains(className);
            sync(collapsed);
            writePreference(key, collapsed);
        });
    });
    const themeToggle = document.getElementById('dark-mode-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('keydown', function (event) {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                themeToggle.click();
            }
        });
    }
})();
