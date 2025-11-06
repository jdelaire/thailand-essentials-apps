document.addEventListener('DOMContentLoaded', () => {
  const backToTop = document.querySelector('[data-back-to-top]');
  const navLinks = document.querySelectorAll('[data-nav-link]');
  const sections = Array.from(document.querySelectorAll('[data-section]'));
  const primaryNav = document.querySelector('.primary-nav');

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
    if (!primaryNav) return;
    const { scrollLeft, scrollWidth, clientWidth } = primaryNav;
    const atStart = scrollLeft <= 2;
    const atEnd = scrollLeft + clientWidth >= scrollWidth - 2;
    primaryNav.classList.toggle('show-left-shadow', !atStart);
    primaryNav.classList.toggle('show-right-shadow', !atEnd);
  };

  const evaluateNavOverflow = () => {
    if (!primaryNav) return;
    const isScrollable = primaryNav.scrollWidth - primaryNav.clientWidth > 1;
    if (isScrollable) {
      primaryNav.classList.add('is-scrollable');
      updateNavShadows();
    } else {
      primaryNav.classList.remove('is-scrollable', 'show-left-shadow', 'show-right-shadow');
    }
  };

  if (primaryNav) {
    primaryNav.addEventListener('scroll', updateNavShadows, { passive: true });
    window.addEventListener('resize', evaluateNavOverflow);
    evaluateNavOverflow();
  }

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
});
