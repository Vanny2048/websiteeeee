# EDEN USA — Static Site

Simple, fast static website with a services grid and a Netlify-powered "Request a Quote" form.

## Tech
- Plain HTML/CSS/JS in `site/`
- Netlify Forms (no backend)

## Local development
Open `site/index.html` in your browser, or serve the folder:

```bash
cd site
python3 -m http.server 3000
# visit http://localhost:3000
```

## Deploy to Netlify
This repo includes `netlify.toml` so Netlify publishes the `site/` folder.

1. Push to GitHub/GitLab/Bitbucket
2. In Netlify, pick "Add new site" → "Import an existing project"
3. Set:
   - Build command: (leave empty)
   - Publish directory: `site`
4. Deploy

### Netlify Forms
The quote form is already wired up:

```html
<form name="quote" method="POST" netlify data-netlify="true" netlify-honeypot="bot-field" action="/success.html">
  <input type="hidden" name="form-name" value="quote" />
  ...
</form>
```

Submissions will appear in Netlify → Forms → `quote`. You can connect notifications (email, Slack, Zapier, etc.).

## Editing content
- Services live in `site/index.html` under the `#services` section.
- Images use royalty-free Unsplash placeholders; replace `src` URLs if desired.

## Useless files removed
Only the necessary files are kept:

```
site/
  index.html
  styles.css
  script.js
  success.html
netlify.toml
README.md
```

## License
All sample images are from Unsplash per their license; replace for production use.