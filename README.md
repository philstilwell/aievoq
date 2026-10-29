# AIEVOQ — AI Evolution Quarterly

The public website for **https://aievoq.com**: an illustrated quarterly exploring AI through an evolutionary-biology analogy, by Phil Stilwell.

## Website

This is a small static site: `index.html`, `styles.css` and local artwork. There are no package dependencies, build steps, forms, trackers or server services.

The homepage introduces the first issue through three lead stories, the demand section, six recurring departments, the fictional species, and the editorial approach. The issue remains in preparation for the end of 2026. The issue preview now includes the statistical census developed for review draft 0.17; it does not serve the working PDF.

The three fictional species illustrations and four supporting scenes were created for this project using built-in ImageGen. The website uses lightweight WebP copies; the original report and full-resolution artwork are maintained separately. No new images were generated for the website expansion.

The design echoes the report with charcoal, cobalt, ivory and copper; small capsule illustrations with 3px borders; softly rounded information panels; subtle shadows; and large unframed artwork with fading edges. Native HTML disclosure controls provide optional extra detail without JavaScript. The statistics page progressively adds SVG charts and two display controls; its tables and downloads remain available without JavaScript. System fonts avoid external font requests.

## Content and artwork

- `index.html`: issue preview, recurring departments and publication status.
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

Serve this directory with any static web server, for example `python3 -m http.server 4173`, then open `http://localhost:4173`.

© 2026 Phil Stilwell. No additional license is granted for the text or artwork.

## Article openings

Every article and substantive feature begins with an **AI concept** panel that defines the real AI subject before the biological comparison. Use ordinary language and explain why the distinction matters. Keep the label and styling consistent with the magazine. The issue page has ten panels, and the statistical census has six. Article length remains flexible during development; do not compress copy merely to match a prior layout.
