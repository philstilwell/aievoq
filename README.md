# AIEVOQ — AI Evolution Quarterly

The public placeholder website for **https://aievoq.com**: an illustrated quarterly exploring AI through an evolutionary-biology analogy, by Phil Stilwell.

## Website

This is a small static site: `index.html`, `styles.css` and local artwork. There are no package dependencies, build steps, forms, trackers or server services.

The three fictional species illustrations were created for this project using built-in ImageGen. The website uses WebP copies; the original report and full-resolution artwork are maintained separately.

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
