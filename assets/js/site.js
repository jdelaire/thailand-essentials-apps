document.addEventListener('DOMContentLoaded', () => {
  const backToTop = document.querySelector('[data-back-to-top]');
  const navLinks = document.querySelectorAll('[data-nav-link]');
  const sections = Array.from(document.querySelectorAll('[data-section]'));

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
