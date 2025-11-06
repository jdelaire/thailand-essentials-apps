# 🇹🇭 Thailand Essential Apps (Static Edition)

A single-page static site that curates the must-have apps for travelers, expats, and digital nomads living in Thailand. The project now ships as plain HTML/CSS/JS—no static site generators or Markdown builds required.

## 📂 Project Structure

```
thailand-essentials-apps/
├── assets/
│   ├── css/
│   │   └── style.css        # Primary theme styling
│   └── js/
│       └── site.js         # Minor interactivity (nav highlights, back-to-top)
├── icons/                   # 64×64 (or larger) app icons
├── screenshots/             # 392×696 App Store portrait screenshots
├── index.html               # Main content (sections + app cards)
├── AGENTS.md                # Contributor guidelines for automated agents
└── scripts/                 # Utility scripts (e.g., App Store screenshot fetcher)
```

## 🚀 Previewing the Site Locally

Because everything is static, you can open `index.html` directly in any modern browser. For a closer match to production paths, run a lightweight server from the project root:

```bash
python3 -m http.server 4000
# then visit http://localhost:4000/
```

## ✍️ Updating Content

1. **Copywriting & Layout** – Edit `index.html`. Each category section (`#transport`, `#money`, etc.) uses `<article class="app-card">` blocks for individual apps.
2. **Icons** – Drop 64×64 (or higher) square images into `icons/`. Keep filenames in lowercase kebab-case (e.g., `deep-pocket.jpg`).
3. **Screenshots** – Add 392×696 portrait JPGs to `screenshots/` following the `{app-name}-{1..3}.jpg` pattern. Update the corresponding `<div class="screenshot-strip">` references.
4. **Styling tweaks** – Adjust `assets/css/style.css`. The palette and layout borrow cues from [ThaiQuest](https://www.thaiquest.site), using Plus Jakarta Sans and Inter.
5. **Interactions** – Minimal behavior (nav highlighting, back-to-top button) lives in `assets/js/site.js`.

## 🧩 Design Notes

- Dark, neon-accented aesthetic inspired by ThaiQuest.
- Responsive grid layout (`.app-grid`) automatically adapts to mobile.
- Intersection Observer highlights the active navigation link while scrolling.
- Buttons and tags reuse gradients/accents defined in the CSS root variables.

## 📦 Deployment

Serve `index.html` from any static host (GitHub Pages, Netlify, Vercel, S3, nginx, etc.). No build step is necessary—push the updated HTML/CSS/JS and you’re live.

## 📄 License

Released under the [MIT License](LICENSE). Attribution is appreciated if you fork or remix the guide.
