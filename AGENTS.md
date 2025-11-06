# Repository Guidelines (Static Site)

## Structure & Responsibilities
- `index.html` contains all rendered content. Categories are marked with `section` elements (`id="transport"`, `id="money"`, etc.) and each app lives inside an `<article class="app-card">`.
- Styling lives in `assets/css/style.css`. It defines the ThaiQuest-inspired palette, grid, and component styles.
- Light interactivity (navigation highlighting + back-to-top button) is handled by `assets/js/site.js`.
- Icons (`icons/`) should be square, 64×64px minimum, JPG or PNG. Screenshots (`screenshots/`) are portrait 392×696px JPGs.
- `scripts/` holds helper utilities (for example, the App Store screenshot fetcher). Update or extend as needed, but it is not part of the runtime site.

## Local Preview
- Open `index.html` directly in a browser for quick checks.
- For accurate relative paths, run a lightweight server from the project root:
  ```bash
  python3 -m http.server 4000
  ```

## Editing Conventions
- Keep HTML tidy and semantic. Use existing utility classes before introducing new ones.
- For new apps, duplicate an existing `.app-card` and update icon paths, copy, and screenshots. Maintain the `{app-name}-{1..3}.jpg` naming scheme.
- Use descriptive `alt` text on every image.
- Prefer lowercase kebab-case for filenames (`deep-pocket.jpg`, `deep-pocket-1.jpg`).
- When tweaking layout colors or spacing, adjust CSS custom properties at the top of `style.css` so the theme stays cohesive.

## Testing & QA
- There is no automated test suite. Manually verify:
  - Layout on mobile and desktop breakpoints.
  - Navigation anchors scroll to the correct sections.
  - External links open in new tabs and include `rel="noreferrer noopener"`.
  - Back-to-top button appears after scrolling.
- Optimize new images before committing to keep repository size manageable.

## Git Hygiene
- Write imperative, capitalized commit subjects (e.g., `Add DeepPocket payment card`).
- If a change requires manual verification, mention the steps or browsers used in the description.
- Avoid force-pushes to shared branches unless coordinated.
