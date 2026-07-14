<?php
/**
 * Plugin Name: Laser178 Style
 * Description: Темное industrial-оформление в стиле СПЕЦТЕХ для laser178.ru
 * Version: 1.0
 * Author: Hermes
 */

if (!defined('ABSPATH')) exit;

class Laser178_Style {

    public function __construct() {
        add_action('wp_enqueue_scripts', [$this, 'enqueue_styles'], 999);
        add_action('wp_footer', [$this, 'add_canvas']);
        add_action('wp_footer', [$this, 'add_theme_toggle'], 999);
        add_action('wp_head', [$this, 'preload_fonts']);
    }

    /* Lightbox logic moved to laser178-lightbox.js */

    public function enqueue_styles() {
        $css_ver = filemtime(plugin_dir_path(__FILE__) . 'laser178-style.css') ?: '2.1';
        wp_enqueue_style('laser178-style', plugins_url('laser178-style.css', __FILE__), [], $css_ver);
        wp_enqueue_style('laser178-fonts', 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap', [], '1.0');
        wp_enqueue_script('laser178-lightbox', plugins_url('laser178-lightbox.js', __FILE__), [], '1.1', true);
        wp_enqueue_script('pdfmake', 'https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.12/pdfmake.min.js', [], '0.2.12', true);
        wp_enqueue_script('pdfmake-fonts', 'https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.12/vfs_fonts.js', [], '0.2.12', true);
        wp_enqueue_script('laser178-pdf', plugins_url('laser178-calculator-pdf.js', __FILE__), ['pdfmake', 'pdfmake-fonts'], '1.3', true);
    }

    public function add_theme_toggle() {
        // Disabled: theme toggle removed, dark theme only
    }

    public function preload_fonts() {
        echo '<link rel="preconnect" href="https://fonts.googleapis.com">';
        echo '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>';
        echo '<script>(function(){document.documentElement.setAttribute("data-theme","dark");try{localStorage.removeItem("laser178_theme");}catch(e){}})();</script>';
    }

    public function add_canvas() {
        if (is_front_page()) {
            echo '<canvas id="laser-canvas"></canvas>';
            echo '<script>
(function() {
    const canvas = document.getElementById("laser-canvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    let width, height;
    function resize() {
        width = canvas.width = canvas.parentElement ? canvas.parentElement.offsetWidth : window.innerWidth;
        height = canvas.height = canvas.parentElement ? canvas.parentElement.offsetHeight : window.innerHeight;
    }
    resize();
    window.addEventListener("resize", resize);
    const particles = [];
    for (let i = 0; i < 40; i++) {
        particles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5,
            size: Math.random() * 2 + 1
        });
    }
    function draw() {
        ctx.clearRect(0, 0, width, height);
        ctx.fillStyle = "rgba(0, 200, 240, 0.6)";
        particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;
            if (p.x < 0 || p.x > width) p.vx *= -1;
            if (p.y < 0 || p.y > height) p.vy *= -1;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
        });
        // Connect nearby particles
        ctx.strokeStyle = "rgba(0, 200, 240, 0.08)";
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 120) {
                    ctx.lineWidth = 1 - dist / 120;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(draw);
    }
    draw();
})();
            </script>';
        }
    }
}

new Laser178_Style();
