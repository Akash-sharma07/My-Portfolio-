# Akash Sharma — AI/ML Portfolio

This repository contains a personal portfolio for Akash Sharma, an aspiring AI/ML Engineer and Data Scientist. It presents his background, skills, projects, and contact details in the existing responsive design.

## Portfolio pages

- **Home:** Introduction, profile photo, selected work, and technology marquee.
- **About:** Education, learning journey, and credentials.
- **Skills:** Programming, machine learning, deep learning, Generative AI, analytics, and tools.
- **Projects:** Three featured projects with individual detail pages.
- **Talk With Me:** Contact details and a Formspree contact form.

## Featured projects

- **AI Admissions Chatbot — ITM University Gwalior:** Answers prospective student questions using university-specific PDFs and documents. Technologies: Python, LangChain, LangGraph, prompt engineering, and Streamlit.
- **Recommendify:** Combines book and movie recommendations in one application, including TF-IDF/cosine similarity for books and content-based recommendations using TMDB movie data. Technologies: Python, Pandas, NumPy, Scikit-learn, Flask, and the TMDB API.
- **Flight Database Analysis:** Extracts and analyzes flight data from MySQL, then presents it in an interactive interface. Technologies: Python, SQL, MySQL, PyMySQL, Pandas, and Streamlit.

These descriptions and the existing GitHub/live demo URLs come from the portfolio source templates.

The source templates themselves label the ITM chatbot repository/demo, Flight Management repository, and Recommendify repository/demo URLs as needing confirmation. Their current URLs are preserved in the site; verify or replace them in the corresponding files under `public/projects/` before treating them as final. The ITM demo link is also shown on the homepage.

## Technologies

The deployed portfolio itself uses semantic HTML, the existing separate CSS stylesheets, and vanilla JavaScript. Render hosts the static files; Formspree handles new contact submissions after its form ID is configured. No frontend framework or database is required to serve the portfolio.

## Static site on Render

The deployable site is in `public/`. It contains ordinary HTML, separate page stylesheets, JavaScript, images, the favicon, and a `404.html` page. Render serves these files directly; the deployed site does not run Flask, Jinja2, SQLAlchemy, MySQL, PostgreSQL, SQLite, Gunicorn, sessions, or database environment variables.

Create a **Static Site** in Render and connect this repository and the branch you want to publish. Use these settings:

| Setting | Value |
|---|---|
| Root Directory | Leave blank |
| Build Command | Leave blank; there is no build step |
| Publish Directory | `public` |
| Environment Variables | None required |

Render serves static sites over its CDN. See [Render Static Sites](https://render.com/docs/static-sites) and [Render's first deployment guide](https://render.com/docs/your-first-deploy).

The original Flask source, templates, models, and requirements are retained in the repository for reference and for any future backend use. They are outside the published `public/` directory. The existing local database and its data were not accessed or changed.

For the static deployment, these backend pieces are no longer needed to serve the portfolio: `app.py` and its Flask routes, `models/` and SQLAlchemy, the MySQL/PyMySQL configuration, `manage_admin.py`, Flask sessions, Gunicorn, and the admin login/dashboard templates. The admin pages and their styles are not copied into `public/`.

## Configure the contact form

The static form sends **Name, Email, Purpose, and Message** to Formspree over HTTPS. It validates required fields and email format in the browser, includes a honeypot, prevents duplicate submissions while sending, and displays accessible inline success or error feedback. It reports success only after Formspree confirms the request.

The form is intentionally unconfigured until you add your own Formspree form ID. With the placeholder still present, trying to send a message displays a setup warning instead of claiming the message was delivered.

1. Create or sign in to an account at [Formspree](https://formspree.io/), verify your email, and create a new form.
2. Open that form's **Integration** page and copy its endpoint. Formspree documents this in [Building an HTML Form](https://help.formspree.io/articles/building-your-form/building-an-html-form).
3. In `public/contact.html`, find the contact form's `action` attribute:

   ```html
   action="https://formspree.io/f/YOUR_FORM_ID"
   ```

   Replace `YOUR_FORM_ID` with the ID from your Formspree endpoint. Keep the `https://formspree.io/f/` prefix. This is the only endpoint setting; no API key or email password belongs in the website code.
4. Commit and push the change so Render deploys the configured page.
5. Submit a test message from the deployed site. Confirm it appears in your Formspree dashboard and adjust the notification recipient/settings there. Formspree stores submissions in that dashboard; they are not sent to the old MySQL database.

The browser-side form behavior follows Formspree's [JavaScript/AJAX guidance](https://help.formspree.io/articles/building-your-form/submit-forms-with-javascript-ajax). This repository has not been tested against a real form endpoint because no Formspree ID has been configured.

## Editing the portfolio

For the Render static site, edit the relevant HTML directly in `public/`:

- `public/index.html`
- `public/about.html`
- `public/skills.html`
- `public/projects.html`
- `public/contact.html`
- `public/projects/ai-admissions-chatbot.html`
- `public/projects/flight-database-analysis.html`
- `public/projects/recommendify.html`

Page-specific CSS remains in `public/css/`; shared behavior is in `public/js/main.js`; images are in `public/images/`. Local-root paths in the HTML (such as `/css/base.css`) work from the nested project detail URLs as well as the top-level pages. Keep the page markup and class names when changing content so the current design and responsive behavior continue to apply.

To preview the published files locally from PowerShell, run `py -m http.server 8000 --directory public` from the repository root, then open `http://localhost:8000`. Python is only used for this optional local preview, not to build or serve the deployed site.

## Resume file

There is currently no resume PDF in `static/`, so the existing resume controls remain visible but are disabled in the static pages. To enable them, add your PDF as `public/Akash_Sharma_Resume.pdf` and change the two disabled resume links in `public/index.html` and the shared navigation on the other pages to point to `/Akash_Sharma_Resume.pdf`.

## What changes with static hosting

- The public static site does not include the admin login or dashboard. A browser-side password screen would not secure private data.
- New contact submissions are managed in Formspree. Existing messages, if any, remain in the old database and have not been migrated.
- The Flask application, SQLAlchemy models, and database are not needed to serve the static site. They remain outside `public/` and have not been deleted.
- Existing GitHub, LinkedIn, email, and project URLs were retained as present in the source templates. No new profile or project URLs were invented.
- The contact form cannot deliver messages until you replace the Formspree placeholder and deploy that change.

## Verification status

The static pages were generated from the existing public templates and assets. Local checks should confirm there is no Jinja syntax in `public/`, that local page and asset links resolve, and that the public directory contains no Flask admin pages or environment files. A real Formspree submission and the live Render deployment cannot be verified until you configure the endpoint and deploy the static site.
