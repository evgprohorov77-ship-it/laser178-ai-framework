(function() {
    var grid = document.querySelector('.laser-works-grid[data-lightbox="works"]');
    if (!grid) return;
    var items = Array.from(grid.querySelectorAll('.laser-works-item'));
    var lightbox = document.getElementById('laserLightbox');
    var img = document.getElementById('laserLightboxImg');
    var current = 0;
    function show(i) {
        current = i;
        var thumb = items[current].querySelector('img');
        img.src = items[current].dataset.full;
        img.alt = thumb ? thumb.alt : '';
        img.style.transform = thumb ? (window.getComputedStyle(thumb).transform || 'none') : 'none';
        lightbox.classList.add('active');
        lightbox.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
    }
    function close() {
        lightbox.classList.remove('active');
        lightbox.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
        img.style.transform = '';
    }
    function next() { show((current + 1) % items.length); }
    function prev() { show((current - 1 + items.length) % items.length); }

    function getItem(el) {
        while (el && el !== grid) {
            if (el.classList && el.classList.contains('laser-works-item')) return el;
            el = el.parentNode;
        }
        return null;
    }

    function isTouchDevice() {
        return window.matchMedia('(pointer: coarse)').matches;
    }

    if (isTouchDevice()) {
        var startX = 0, startY = 0, startTime = 0, moved = false, startItem = null;
        var TAP_THRESHOLD = 10;
        var TIME_THRESHOLD = 300;

        grid.addEventListener('touchstart', function(e) {
            var t = e.touches[0];
            startX = t.clientX;
            startY = t.clientY;
            startTime = Date.now();
            moved = false;
            startItem = getItem(e.target);
        }, {passive: true});

        grid.addEventListener('touchmove', function(e) {
            if (!startItem) return;
            var t = e.touches[0];
            var dx = t.clientX - startX;
            var dy = t.clientY - startY;
            if (Math.abs(dx) > TAP_THRESHOLD || Math.abs(dy) > TAP_THRESHOLD) {
                moved = true;
                startItem = null;
            }
        }, {passive: true});

        grid.addEventListener('touchend', function(e) {
            var item = getItem(e.target);
            if (!item || !startItem || item !== startItem) return;
            if (moved) return;
            if (Date.now() - startTime > TIME_THRESHOLD) return;
            e.preventDefault();
            var idx = items.indexOf(item);
            if (idx >= 0) show(idx);
            startItem = null;
        });

        grid.addEventListener('touchcancel', function() {
            startItem = null;
            moved = true;
        });
    } else {
        items.forEach(function(item, i) {
            item.addEventListener('click', function(e) { e.preventDefault(); show(i); });
            item.addEventListener('keydown', function(e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); show(i); } });
        });
    }

    lightbox.querySelector('.laser-lightbox-close').addEventListener('click', close);
    lightbox.querySelector('.laser-lightbox-next').addEventListener('click', function(e) { e.stopPropagation(); next(); });
    lightbox.querySelector('.laser-lightbox-prev').addEventListener('click', function(e) { e.stopPropagation(); prev(); });
    lightbox.addEventListener('click', function(e) { if (e.target === lightbox) close(); });
    document.addEventListener('keydown', function(e) {
        if (!lightbox.classList.contains('active')) return;
        if (e.key === 'Escape') close();
        if (e.key === 'ArrowRight') next();
        if (e.key === 'ArrowLeft') prev();
    });
})();
