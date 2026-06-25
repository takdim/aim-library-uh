/* ============================================================
   UniLib — main.js
   Scroll reveal, animated counters, parallax, navbar scroll
   Uses IntersectionObserver (no window.addEventListener scroll
   for reveal — only for navbar blur which is lightweight)
   ============================================================ */

'use strict';

// ── Scroll Reveal via IntersectionObserver ───────────────────
const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');

        // Trigger counters inside this element
        entry.target.querySelectorAll('[data-counter]').forEach((el) => {
          animateCounter(el);
        });

        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12 }
);

document.querySelectorAll('.reveal-on-scroll').forEach((el) => {
  revealObserver.observe(el);
});

// ── Animated Number Counter ──────────────────────────────────
function animateCounter(el) {
  const target = parseInt(el.dataset.counter, 10);
  if (isNaN(target)) return;

  const duration = 1800; // ms
  const startTime = performance.now();

  // Ease-out cubic
  const easeOut = (t) => 1 - Math.pow(1 - t, 3);

  const step = (now) => {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const current = Math.round(easeOut(progress) * target);
    el.textContent = current.toLocaleString('id-ID') + (progress < 1 ? '' : '+');
    if (progress < 1) requestAnimationFrame(step);
  };

  requestAnimationFrame(step);
}

// ── Navbar: glass intensifies on scroll ──────────────────────
const nav = document.getElementById('main-nav');
if (nav) {
  const handleScroll = () => {
    if (window.scrollY > 60) {
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }
  };
  // Passive listener — minimal perf cost
  window.addEventListener('scroll', handleScroll, { passive: true });
}

// ── Mouse Parallax for hero blobs ────────────────────────────
// Uses transform only (hardware accelerated, no layout thrash)
const parallaxEls = document.querySelectorAll('.parallax-element');
if (parallaxEls.length && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  document.addEventListener('mousemove', (e) => {
    const cx = window.innerWidth / 2;
    const cy = window.innerHeight / 2;
    const dx = (e.clientX - cx) / cx; // -1 to 1
    const dy = (e.clientY - cy) / cy;

    parallaxEls.forEach((el) => {
      const speed = parseFloat(el.dataset.speed) || 1;
      const tx = dx * speed * 18;
      const ty = dy * speed * 18;
      el.style.transform = `translate(${tx}px, ${ty}px)`;
    });
  });
}

// ── Mobile Hamburger Menu ────────────────────────────────────
const hamburger = document.getElementById('hamburger-btn');
const mobileMenu = document.getElementById('mobile-menu');
if (hamburger && mobileMenu) {
  const hamburgerIcon = hamburger.querySelector('.material-symbols-outlined');
  
  hamburger.addEventListener('click', () => {
    const isClosed = mobileMenu.classList.toggle('hidden');
    hamburger.setAttribute('aria-expanded', String(!isClosed));
    
    // Change icon to close when menu is open
    if (hamburgerIcon) {
      hamburgerIcon.textContent = isClosed ? 'menu' : 'close';
    }
    
    // Adjust border-radius so container doesn't become a giant circle
    if (nav) {
      if (isClosed) {
        nav.classList.remove('rounded-[2rem]');
        nav.classList.add('rounded-full');
      } else {
        nav.classList.remove('rounded-full');
        nav.classList.add('rounded-[2rem]');
      }
    }
  });

  // Close mobile menu when clicking any link inside it
  mobileMenu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      mobileMenu.classList.add('hidden');
      hamburger.setAttribute('aria-expanded', 'false');
      if (hamburgerIcon) {
        hamburgerIcon.textContent = 'menu';
      }
      if (nav) {
        nav.classList.remove('rounded-[2rem]');
        nav.classList.add('rounded-full');
      }
    });
  });
}

// ── Auto-close flash messages ────────────────────────────────
document.querySelectorAll('.flash-message').forEach((msg) => {
  const closeBtn = msg.querySelector('[data-dismiss]');
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      msg.style.opacity = '0';
      msg.style.transform = 'translateY(-8px)';
      setTimeout(() => msg.remove(), 300);
    });
  }
  // Auto-dismiss after 5s
  setTimeout(() => {
    msg.style.transition = 'opacity 0.5s, transform 0.5s';
    msg.style.opacity = '0';
    msg.style.transform = 'translateY(-8px)';
    setTimeout(() => msg.remove(), 500);
  }, 5000);
});

// ── Dashboard Sidebar Toggle (mobile) ────────────────────────
const sidebarToggle = document.getElementById('sidebar-toggle');
const sidebar = document.getElementById('dash-sidebar');
if (sidebarToggle && sidebar) {
  sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('-translate-x-full');
  });
}
