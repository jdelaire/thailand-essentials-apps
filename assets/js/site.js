document.addEventListener('DOMContentLoaded', () => {
  const backToTop = document.querySelector('[data-back-to-top]');
  const navLinks = document.querySelectorAll('[data-nav-link]');
  const sections = Array.from(document.querySelectorAll('[data-section]'));
  const primaryNav = document.querySelector('.primary-nav');
  const navContainer = document.querySelector('.primary-nav-container');

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute('id');
          navLinks.forEach((link) => {
            link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
          });
        }
      });
    },
    {
      rootMargin: '-50% 0px -35% 0px',
      threshold: 0.25,
    }
  );

  sections.forEach((section) => observer.observe(section));

  const updateNavShadows = () => {
    if (!primaryNav || !navContainer) return;
    const { scrollLeft, scrollWidth, clientWidth } = primaryNav;
    const atStart = scrollLeft <= 2;
    const atEnd = scrollLeft + clientWidth >= scrollWidth - 2;
    navContainer.classList.toggle('show-left-shadow', !atStart);
    navContainer.classList.toggle('show-right-shadow', !atEnd);
  };

  const evaluateNavOverflow = () => {
    if (!primaryNav || !navContainer) return;
    const isScrollable = primaryNav.scrollWidth - primaryNav.clientWidth > 1;
    if (isScrollable) {
      navContainer.classList.add('is-scrollable');
      updateNavShadows();
    } else {
      navContainer.classList.remove('is-scrollable', 'show-left-shadow', 'show-right-shadow');
    }
  };

  if (primaryNav && navContainer) {
    primaryNav.addEventListener('scroll', updateNavShadows, { passive: true });
    window.addEventListener('resize', evaluateNavOverflow);
    evaluateNavOverflow();
  }

  const getNavOffset = () => {
    const header = document.querySelector('.site-header');
    const headerHeight = header ? header.getBoundingClientRect().height : 0;
    return headerHeight + 24;
  };

  const scrollToHash = (hash, { smooth = true } = {}) => {
    if (!hash || !hash.startsWith('#')) return;
    const target = document.querySelector(hash);
    if (!target) return;

    const offset = getNavOffset();
    const top = Math.max(target.getBoundingClientRect().top + window.scrollY - offset, 0);
    window.scrollTo({
      top,
      behavior: smooth ? 'smooth' : 'auto',
    });

    if (history.replaceState) {
      history.replaceState(null, '', hash);
    } else {
      window.location.hash = hash.slice(1);
    }
  };

  navLinks.forEach((link) => {
    link.addEventListener('click', (event) => {
      const href = link.getAttribute('href');
      if (!href || !href.startsWith('#')) return;
      event.preventDefault();
      scrollToHash(href, { smooth: true });
    });
  });

  const toggleBackToTop = () => {
    if (!backToTop) return;
    const shouldShow = window.scrollY > 360;
    backToTop.classList.toggle('visible', shouldShow);
  };

  toggleBackToTop();
  window.addEventListener('scroll', toggleBackToTop, { passive: true });

  backToTop?.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  if (window.location.hash) {
    scrollToHash(window.location.hash, { smooth: false });
  }
});
