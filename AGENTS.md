# Repository Guidelines

## Project Structure & Module Organization
This Jekyll 4 site uses the Just the Docs theme. Top-level Markdown files such as `index.md`, `transport.md`, and `money.md` define each content category. Shared components live in `_includes/`, layouts in `_layouts/`, and global settings in `_config.yml`. Visual assets reside in `icons/` (64×64 thumbnails) and `screenshots/` (156×277 galleries), while custom CSS is managed in `assets/css/style.css`. Utility scripts, including `scripts/fetch_appstore_screenshots.py`, support asset automation.

## Build, Test, and Development Commands
Run `bundle install` whenever the Gemfile changes. Use `bundle exec jekyll serve` for a local preview at `http://localhost:4000`, or add `--livereload` while iterating. `bundle exec jekyll build` compiles `_site/` for CI checks, and `bundle exec jekyll clean` clears caches after layout or theme tweaks. Docker users can mirror the workflow with `docker-compose up --build`.

## Coding Style & Naming Conventions
Start every page with YAML front matter (`title`, `nav_order`) followed by one H1. Favor Markdown headings, tables, and emphasis; embed HTML only for structured components such as the `.app-header` pattern in `transport.md`. Keep inline `<style>` tags grouped near the top of a file and reuse existing class names. Name images in lowercase kebab-case (`grab.jpg`, `grab-1.jpg`) and maintain the existing two-space list indentation.

## Testing Guidelines
There is no automated suite, so treat `bundle exec jekyll build` as the required regression test before committing. Use `bundle exec jekyll serve --livereload` to review new copy, verify navigation, and confirm icons or screenshots load correctly. When adjusting asset dimensions or CSS, spot-check mobile breakpoints through browser dev tools.

## Commit & Pull Request Guidelines
Write imperative, capitalized commit subjects (`Update Apple Maps screenshots`). Conventional prefixes such as `feat:` or `fix:` are welcome when they clarify scope; append issue or PR numbers when relevant (`feat: Add Grab tips (#5)`). Pull requests should describe the user-facing impact, list the commands you ran (`bundle exec jekyll build`), and attach refreshed screenshots whenever visuals shift.

## Asset & Content Management Tips
Icons stay at 64×64 with 8px corners, while screenshots remain 156×277 with 10px corners. Source App Store imagery via `scripts/fetch_appstore_screenshots.py`, rename files to `{app-name}-{1..3}.jpg`, and compress them before committing. Maintain descriptive `alt` text and reuse the `.app-screenshot` classes so hover and shadow effects remain consistent.
