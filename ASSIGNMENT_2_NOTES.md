# Movie Lab / Assignment 2

## Website link

- Live website: https://teobodev.github.io/movie-lab/
- Repository: https://github.com/teobodev/movie-lab
- Deployment: GitHub Pages, built and published by `.github/workflows/deploy-pages.yml` on pushes to `main`.
- Deployment verification: the GitHub Actions build-and-deploy run completed successfully on October 3, 2026; the public site loaded at the URL above.

## What changed

- Replaced the starter page with the custom FRAME. identity: near-black cinema palette, editorial serif headlines, acid-green accents, film-grain-like layered lighting, compact mono labels, and subtle motion.
- Redesigned the API-key connection panel and connected-state search hero, navigation, connection/change-key actions, catalog headings, result metadata, and footer.
- Rebuilt movie cards with responsive poster artwork, hover treatment, numbered frames, rating chips, release-year metadata, readable overview excerpts, TMDB links, and an artwork fallback.
- Added purpose-designed loading skeletons, no-results guidance, and actionable API error/retry panels; retained real TMDB popular/search data, request cancellation, pagination, and in-memory-only key handling.
- Added visible focus states, reduced-motion support, responsive grids, page metadata, and a matching favicon.

## Run and build

Requires Node.js 22.18+ or 24.12+.

```sh
npm ci
npm run dev
npm run build
npm run preview
```

The production files are written to `dist/`. Each visitor supplies their own TMDB API Key (v3); it stays in tab memory and is cleared on reload or when changing keys.

## Verification performed

- Production build: `npm run build` completed successfully.
- With a valid key in the browser session: popular movies loaded, a Dune search returned real results, and the result pager advanced to page 2.
- A no-match title showed the empty-search state; a deliberately invalid key showed TMDB's rejected-key message and retry action.
- Mobile viewport checked at 390px; an overflow issue was corrected. Browser console was checked after adding the favicon.
- Real UI captures used by the report are in `screenshots/`.

## Screenshot index

- `screenshots/connection.jpg` — API-key welcome screen.
- `screenshots/popular.jpg` — connected popular catalog and live movie posters.
- `screenshots/search.jpg` — live Dune search results.
- `screenshots/empty.jpg` — zero-match state.
- `screenshots/error.jpg` — invalid API-key error and retry state.
- `screenshots/mobile.png` — 390px responsive welcome screen.

## Maintainer

Maintained by [teobodev](https://github.com/teobodev).
