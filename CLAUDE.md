# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Felipe Duarte's personal site (felipedu.art) — a Jekyll static site hosted on GitHub Pages (repo `felipedreis.github.io`, CNAME `felipedu.art`). It's a CV/portfolio/blog: home page, CV, projects, publications, and a blog of paper-review posts.

## Commands

```bash
bundle install                  # install gems (first time / after Gemfile changes)
bundle exec jekyll serve        # local dev server with live reload, http://localhost:4000
bundle exec jekyll serve --drafts   # also render posts from _drafts/
bundle exec jekyll build        # build static site into _site/
```

There is no test suite, linter, or CI config in this repo — `_site/` is the committed/generated build output, not something to hand-edit.

## Architecture

Standard Jekyll structure, driven almost entirely by three YAML data files under `_data/` rather than hardcoded HTML:

- `_data/cv.yml` — profile blurb, languages, skills, jobs (current/past), education, and social links (`site.data.cv.github`, `site.data.cv.linkedin`). Rendered by `cv.html`.
- `_data/projects.yml` — project list (name, short/description, start/end, repo, thumbnail). Rendered by `projects.html`.
- `_data/publications.yml` — papers (title, doi, abstract, authors, journal, link, file, thumbnail, year, bibtex). Rendered by `publications.html`.

`projects.html` and `publications.html` render a card grid from their data file and use a shared Bootstrap-modal pattern: each card's "Details" button carries the item's fields as `data-bs-*` attributes, and a small inline `<script>` in the same file copies them into the modal on `show.bs.modal`. Follow this pattern (data file + card loop + data-attribute modal) when extending either page rather than inventing a new mechanism. `publications.html` additionally has a bibtex modal with copy-to-clipboard.

Blog posts live in `_posts/` (mostly reviews of ML/NLP papers — attention, word2vec, GPT, etc.) and unpublished ones in `_drafts/` (only rendered with `--drafts`). Post front matter convention:

```yaml
layout: post
title: "..."
date:   YYYY-MM-DD HH:MM:SS +0100
categories: blog research llms
short_intro: "One-line summary shown on the /blog/ index"
highlights:            # optional bullet list rendered in a callout box above the post body
    - ...
thumbnail: images/....png   # optional; falls back to _includes/thumbnail.html (plain gray SVG)
```

`blog/index.html` (layout `long`) lists `site.posts`, grouped by year, using `short_intro`/`thumbnail` from front matter. Pagination is configured (`jekyll-paginate`, 3 posts/page, `/blog/page:num/`) but the index template itself does not currently iterate `paginator` — check this before assuming paged navigation works.

There are two page layouts, both under `_layouts/`, sharing the same header/nav/footer chrome and CDN-loaded Bootstrap 5 + Bootstrap Icons + MathJax:
- `default.html` — full-height centered "cover" layout, used by `index.html`.
- `long.html` — scrollable layout for content-heavy pages (`blog/index.html`, `cv.html`, `projects.html`, `publications.html`, `post.html` extends this pattern too via its own header).

`_layouts/post.html` extends the long-page look with an article title, "Written by Felipe on {date}" byline, and the optional `highlights` callout, then renders the Markdown post body. MathJax is loaded on every page for LaTeX in post content.

Site-wide config (title, url, plugins, `site.data.*` availability) is in `_config.yml`. Note `title`/`email`/`description` there are still Jekyll's default placeholder values, not real content.
