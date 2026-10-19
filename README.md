# Akash Sharma | AI/ML & Data Science

Hi, I'm Akash Sharma. I studied Commerce at Jiwaji University in Gwalior, then became interested in how data and software can solve practical problems. I'm now building my skills in Data Science, Machine Learning, and Generative AI through coursework and hands-on projects.

I'm looking for entry-level AI/ML roles and internships where I can keep learning and contribute to useful work.

## Projects

### AI Admissions Chatbot - ITM University Gwalior
A conversational assistant that answers prospective students' questions using university documents. I built it with Python, LangChain, LangGraph, prompt engineering, and Streamlit.

[View the project page](public/projects/ai-admissions-chatbot.html)

### Recommendify
A book and movie recommendation application. The project brings together TF-IDF and cosine similarity for book recommendations and movie recommendations based on TMDB data.

**Tools:** Python, Pandas, NumPy, Scikit-learn, Flask, TMDB API

[View the project page](public/projects/recommendify.html)

### Flight Database Analysis
An interactive application for querying and exploring flight data stored in MySQL, using SQL and Pandas for the data work and Streamlit for the interface.

**Tools:** Python, SQL, MySQL, PyMySQL, Pandas, Streamlit

[View the project page](public/projects/flight-database-analysis.html)

## Skills I've practiced

- **Programming:** Python, C, object-oriented programming
- **Machine Learning:** Scikit-learn, supervised learning, regression, classification, exploratory data analysis, feature engineering, model evaluation, cross-validation, natural language processing
- **Deep Learning:** TensorFlow, Keras, ANN, CNN, RNN, Transformers
- **Generative AI:** LLMs, prompt engineering, LangChain, LangGraph, RAG, FAISS, Model Context Protocol (MCP)
- **Data:** SQL, MySQL, Pandas, NumPy, Matplotlib, Seaborn, data visualization
- **Application tools:** Flask, FastAPI, Streamlit, Docker, Git, GitHub, Jupyter Notebook, VS Code

## Contact

- **Email:** [akash8017sharma@gmail.com](mailto:akash8017sharma@gmail.com)
- **GitHub:** [github.com/Akash-sharma07](https://github.com/Akash-sharma07)

## About this website

This repository contains my portfolio website. The published version is a static site made with HTML, CSS, and JavaScript. It keeps the original page design and includes Home, About, Skills, Projects, and Contact pages.

Render publishes the files in `public/` as a Static Site. Flask, Jinja, SQLAlchemy, and MySQL are not needed to serve the published pages. The original Flask source and models remain in the repository, outside `public/`, for reference. The local database has not been changed.

### Render settings

Create a Static Site connected to this repository and choose the branch you want to publish:

| Setting | Value |
|---|---|
| Root Directory | Leave blank |
| Build Command | Leave blank |
| Publish Directory | `public` |
| Environment Variables | None required |

### Contact form setup

The contact page uses Formspree. It is not ready to send messages until you add your own form ID:

1. Create a form in your [Formspree account](https://formspree.io/).
2. Copy the form endpoint from its Integration page.
3. In `public/contact.html`, replace `YOUR_FORM_ID` in `https://formspree.io/f/YOUR_FORM_ID` with your form ID.
4. Deploy the change and send a test message. Check the Formspree dashboard to confirm it arrived and set up notifications there if you want them.

The form shows a setup notice while the placeholder remains. It only shows a success message after Formspree accepts a submission. No API key should be added to the website.

### Local preview

From the repository root, run `py -m http.server 8000 --directory public`, then open `http://localhost:8000`. This is only for previewing the static files locally; Render does not need Python to serve them.

## A few notes

- The static site does not have the old admin login or dashboard. New contact messages are handled in Formspree; existing database messages have not been moved.
- There is no resume PDF in the repository right now, so the resume links are disabled. Add `public/Akash_Sharma_Resume.pdf` to make the download available.
- Some existing project repository and demo links in the site were marked for confirmation in the original templates. I've kept those URLs as they were; they should be checked before sharing as final links.
