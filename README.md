# AIEVOQ — AI Evolution Quarterly

The public website for **https://aievoq.com**: an illustrated quarterly exploring AI through an evolutionary-biology analogy, by Phil Stilwell.

## Website

This is a static webzine with local artwork, full reading pages and a statistical census. There are no package dependencies, trackers or server services. The contents search runs in the browser; all articles and sources remain readable without JavaScript.

The complete developing first issue is at `/issues/2026-q4/`. Draft 0.24 contains 56 articles and field notes, plus front matter and workshop notes, 35 Key statistics panels, 112 numbered sources, all 25 illustrated scenes, the species and human casts, and all 23 figure placements. The contents page supports full manuscript search and department filtering. Each reading page has a permanent URL and previous/next links; citations open the matching source entry. The homepage links to the full articles.

The publication is web first. Q4 remains in progress, with selected evidence reviewed through October 30, 2026 and November–December still open. The preserved manuscript and artwork support a possible later print edition. The working PDF remains in the editorial workspace.

The web edition reuses the three fictional species, all twenty-five illustrated scenes, eight public-figure caricatures and the approved cover. The website uses lightweight WebP copies; charts retain their original vector shapes and labels. The original report and full-resolution artwork are maintained separately. No new images were generated for the migration.

The design echoes the report with charcoal, cobalt, ivory and copper; small capsule illustrations with 3px borders; softly rounded information panels; subtle shadows; and large unframed artwork with fading edges. Native HTML disclosure controls provide optional extra detail without JavaScript. The statistics page progressively adds SVG charts and two display controls; its tables and downloads remain available without JavaScript. System fonts avoid external font requests.

## Content and artwork

- `index.html`: webzine home, featured articles and publication status.
- `issues/2026-q4/`: complete contents, 56 reading sections and the combined source ledger.
- `webzine.css`, `webzine.js`: reading layouts, print stylesheet and optional contents search.
- `content/`: exact versioned manuscript, statistics panels, figure captions and migration inventory.
- `scripts/build_webzine.py`: dependency-free generator for the reading pages, source ledger, search index and sitemap.
- `scripts/check_webzine.py`: content-preservation, citation, image and local-link audit.
- `assets/issue-01/`: optimized copies of approved artwork and vector figures exported from the print source; no new generated art.
- `styles.css`: responsive layouts, accessible focus states and reduced-motion support.
- `statistics/`: permanent census with five charts, source notes, static data tables, CSV downloads and a dated JSON archive. See `statistics/README.md` for the update rules.
- `assets/ledgerfinch.webp`, `relay-octopus.webp`, `proofweaver.webp`: the recurring species.
- `assets/mathematical-rain.webp`, `learning-nursery.webp`, `naturalist-surprised.webp`: capsule illustrations from the existing report.
- `assets/watering-hole.webp`: the established demand scene, also used for social sharing metadata.

The site introduces questions and features without assigning unsupported survival scores, confirming a speciation event, or presenting unfinished quarter-end reporting as final. Keep the imagined cast and conceptual comparisons distinct from documented claims.

## Hosting

GitHub Pages publishes the root of the `main` branch. The `CNAME` file sets `aievoq.com` as the custom domain. Namecheap manages domain registration and DNS.

Expected DNS:

| Type | Host | Value |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | philstilwell.github.io |

Keep existing mail and verification records when updating web routing. HTTPS is provided by GitHub Pages.

## Local review

Rebuild with `python3 scripts/build_webzine.py`, then run `python3 scripts/check_webzine.py`. Serve this directory with any static web server, for example `python3 -m http.server 4173`, then open `http://localhost:4173`.

The generator reads the saved draft in `content/`; never edit generated article HTML by hand. Preserve numbered source versions when revising. The original editorial workspace also contains `production/export_webzine_assets.py`, which reuses the approved print figure definitions, verifies embedded fonts in temporary PDF intermediates, and exports browser-ready SVG figures and WebP artwork. Temporary PDFs are removed automatically. Rebuilding the website from the checked-in source requires only Python's standard library and the retained assets.

© 2026 Phil Stilwell. No additional license is granted for the text or artwork.

## Article openings

Every article and substantive feature begins with an **AI concept** panel that defines the real AI subject before the biological comparison. Use ordinary language and explain why the distinction matters. Keep the label and styling consistent with the magazine. The issue page has ten panels, and the statistical census has six. Article length remains flexible during development; do not compress copy merely to match a prior layout.

## Key statistics panels

Evidence-bearing features have a warm ivory **Key statistics** panel after the concept opening. Six appear on the homepage and six in the census. Each shows named sources and dates, comparisons where supported, and the limits that change interpretation. Definitions come from the magazine’s reviewed article-panel record. The downloadable companion is `statistics/data/article-panels-2026-10-28.json`; the original census data remain unchanged.

Keep observed rates, experimental effects, company evaluations, plans and projections distinct. Never label an experiment, model-version comparison or annual forecast as a quarter-to-quarter trend. If a section has no suitable measured result, omit the panel.

## October 30 editorial update

Draft 0.19 adds one dated Elephant-Goldfish field note and a background-research panel. Four new sources distinguish the launch/documentation from two earlier academic studies. The existing census remains frozen at October 28; none of its readings have been refreshed. The new workflow is not classified as a confirmed species or a measured productivity gain. Existing article URLs are preserved.

Draft 0.20 adds the dedicated elephant-and-goldfish ImageGen plate to the October 22 design article, replacing its temporary office-reef illustration. It illustrates complementary roles without changing the article's evidence or statistical claims.

Draft 0.21 adds The adoption gradient: nine editorial patterns, three side branches, an audit for extraordinary productivity claims and a historically qualified quantum analogy. Its two-study statistics panel distinguishes output per hour from time per task and labels earlier research separately from Q4 evidence. A user-supplied nine-part natural-history overview opens at full size; the existing working-human illustration remains alongside the text. All prior evidence remains preserved.

Draft 0.22 integrates the human-adoption statistics into the feature and the census page. Four responsive charts share one frozen October 30 data record with the print edition: workplace frequency, two-year general-use comparison, non-user barriers and perceived benefits. Three recurring panels retain separate populations, dates and refresh rules. Quarterly workplace comparisons are Q1-to-Q2; other comparisons are explicitly unavailable or two-year changes. JavaScript only switches paired-chart views; all values, tables and downloads remain available without it.

Draft 0.23 added the Linux companion feature, with Q3 statement dating, Q4 policy developments, a disclosed-assistance count, and two academic studies of software forks. The October 14 label-rule change is a measurement break; no new anti-AI lineage or measured productivity gain is asserted. Earlier statistical snapshots are unchanged.

Draft 0.24 retitles that feature "Fork it: the right for purists to branch", adds conditional outlooks for AI-free practices and communities, and introduces the penguin-colony ImageGen plate. It preserves the published article URL. The February 2026 METR update qualifies use of the early-2025 slowdown result; no numerical survival probabilities or lifespans are claimed.
