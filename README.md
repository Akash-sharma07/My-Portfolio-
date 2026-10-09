# Akash Sharma — Personal Portfolio

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript" />
</p>

<p align="center">
  A personal portfolio website where I share my journey into Data Science and AI, showcase projects, and make it easy for recruiters and developers to connect with me.
</p>

<p align="center">
  <strong>AI/ML Engineer Aspirant · Data Science · Generative AI</strong>
</p>

---

## About the Project

This is my personal portfolio website, built with **Flask, Jinja2, HTML, CSS, JavaScript, and MySQL**. It brings my background, technical skills, and hands-on projects together in one place.

The design follows a clean, light, editorial style with readable typography, responsive layouts, and subtle interactions. The aim is to keep the site professional and easy to navigate rather than overload it with unnecessary effects.

The site also includes a contact form backed by a database and a private admin area for reviewing submitted messages.

## What You Can Find Here

- **Home:** A short introduction and direct links to my work.
- **About:** My learning journey from a Commerce background into Data Science and AI.
- **Skills:** Technologies and concepts I have been learning and practising.
- **Projects:** A collection of my hands-on applications, with project details and relevant links.
- **Talk With Me:** A contact form for opportunities, collaborations, feedback, and project discussions.
- **Admin dashboard:** A protected area for reviewing contact-form submissions.
- **Responsive design:** Layouts designed to work across desktop, tablet, and mobile screens.

## Featured Projects

### 1. AI Admissions Chatbot — ITM University Gwalior

A conversational assistant built to answer prospective students' questions using university-specific PDF information. The application uses LangChain for LLM workflow orchestration, LangGraph for workflow/state management, and Streamlit for the interface.

**Technologies:** Python · LangChain · LangGraph · LLMs · Streamlit

### 2. Flight Database Analysis Application

An interactive application for retrieving and analysing flight data from a MySQL database. Python, SQL, and Pandas are used to query, process, and explore the data through a Streamlit interface.

**Technologies:** Python · MySQL · SQL · PyMySQL · Pandas · Streamlit

### 3. Recommendify — Book & Movie Recommendation Platform

A Flask-based platform that brings book and movie recommendations into one application. The book recommender uses TF-IDF and cosine similarity, while the movie recommender uses movie metadata and a TMDB integration to display movie information and posters.

**Technologies:** Python · Pandas · NumPy · Scikit-learn · TF-IDF · Cosine Similarity · Flask · Jinja2 · TMDB API

> Project descriptions are intended to explain each application's purpose and main technologies. For implementation details, code, and demos, see the corresponding project links on the portfolio when available.

## Technology Stack

| Area | Tools and technologies |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML5, CSS3, Vanilla JavaScript, Jinja2 |
| Database | MySQL |
| ORM / database access | Flask-SQLAlchemy, SQLAlchemy, PyMySQL |
| Configuration | Environment variables, `python-dotenv` |
| Production server | Gunicorn |
| Version control | Git, GitHub |
| Deployment | Render for the Flask app; a separately hosted MySQL-compatible database |

The portfolio uses a conventional Flask-rendered frontend rather than a separate React or frontend framework application.

## How It Works

```mermaid
flowchart TD
    A[Visitor] --> B[Flask Portfolio on Render]
    B --> C[Jinja2 Templates]
    C --> D[HTML, CSS and JavaScript]
    B --> E[SQLAlchemy]
    E --> F[(MySQL)]
    A --> G[Contact Form]
    G --> B
    F --> H[Stored Contact Messages]
    I[Admin Login] --> J[Protected Admin Dashboard]
    J --> E
```

The contact form sends the submitted details to the Flask backend. SQLAlchemy handles database operations, and the admin dashboard retrieves stored messages after authentication.

## Run Locally

### Prerequisites

- Python installed on your computer
- MySQL Server installed and running locally
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Akash-sharma07/My-Portfolio-.git
cd akash-portfolio
```

### 2. Create and activate a virtual environment

**Windows PowerShell / Command Prompt:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install and start MySQL Server

Install MySQL Community Server for Windows using the [official MySQL installation guide](https://dev.mysql.com/doc/refman/8.4/en/windows-installation.html). During setup, create or choose a MySQL account and set its password. Start the installed MySQL service from Windows **Services** if it is not already running. MySQL Workbench is optional; you can also use the `mysql` command-line client.

### 5. Create the application database

Connect to MySQL using Workbench or the command-line client, then run:

```sql
CREATE DATABASE portfolio CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Use the account that will be in `DATABASE_URL` and ensure it has privileges on this database. MySQL recommends `utf8mb4` for Unicode data. See the [MySQL character-set guidance](https://dev.mysql.com/doc/refman/8.4/en/charset.html).

### 6. Configure environment variables

Create or update `.env` in the project root. Fill in your actual MySQL username and password; do not assume they are `root` or blank:

```env
DATABASE_URL=mysql+pymysql://YOUR_MYSQL_USER:URL_ENCODED_PASSWORD@localhost:3306/portfolio?charset=utf8mb4
SECRET_KEY=REPLACE_WITH_A_RANDOM_SECRET
ADMIN_USERNAME=YOUR_ADMIN_USERNAME
ADMIN_PASSWORD=YOUR_ADMIN_PASSWORD
```

Replace every example value with your own. URL-encode special characters in the database username or password (for example, `@` becomes `%40`). Keep your existing `SECRET_KEY` and admin settings; do not commit `.env` to GitHub. `.env` is already excluded by `.gitignore`.

To generate a random Flask secret key, run:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the generated value into `SECRET_KEY` in your local `.env` file.

### 7. Install dependencies and start the application

```bash
python -m pip install -r requirements.txt
python app.py
```

On startup, the app connects to the configured MySQL database and creates any missing application tables. It does not drop tables. A new database gets an admin account only when both `ADMIN_USERNAME` and `ADMIN_PASSWORD` are set; the password is stored as a hash.

### 8. Verify the contact form and admin dashboard

Open the local site, submit a valid contact form message, and confirm the success notice appears. In MySQL Workbench or the MySQL client, verify the saved row:

```sql
USE portfolio;
SELECT id, name, purpose, created_at FROM message ORDER BY created_at DESC;
```

Then open `/admin/login`, sign in with the configured admin account, and confirm the message appears in the protected inbox. Records in the original database are not copied by `db.create_all()`, and that database remains untouched. If you need to move records, first make and verify a backup, then copy the `message` and `admin` rows into a staging MySQL database with an explicit migration that stores `created_at` as UTC and preserves each `password_hash` exactly. Compare row counts and sample records, test an admin login, and only then switch production traffic. No data transfer was performed for this change.

## Deployment

The application can be deployed as a Flask web service on Render. The MySQL database must be hosted separately by a cloud provider you choose; Render is used for the Flask web service here, and no cloud database provider or credentials are assumed.

1. Push the project to GitHub.
2. Create a MySQL database with your chosen cloud database provider and follow that provider's instructions for network access and TLS/SSL.
3. Create a Render **Web Service** and connect your GitHub repository.
4. Set the build command to `pip install -r requirements.txt`.
5. Set the start command to `gunicorn app:app` if the Flask instance is named `app` in `app.py`.
6. Add `DATABASE_URL` using the cloud provider's MySQL connection details, plus the required secret/admin environment variables in the Render dashboard. Use the provider's recommended SSL parameters and URL-encode special characters in credentials.
7. Deploy and test the portfolio, contact form, and admin login.

**Important:** Use the cloud MySQL host in Render, never `localhost`. Set the production `DATABASE_URL` in Render's environment settings, not in source control. The application accepts `mysql://` or `mysql+pymysql://` provider URLs and preserves provider SSL options. Keep credentials out of GitHub and check the selected provider's backup, network, and TLS requirements.

Useful links:

- [Render Flask deployment guide](https://render.com/docs/deploy-flask)
- [MySQL 8.4 Reference Manual](https://dev.mysql.com/doc/refman/8.4/en/)

## Project Structure

The following is the intended high-level structure. The exact files in your repository may vary as the project evolves.

```text
portfolio/
├── app.py
├── requirements.txt
├── .env                  # Local secrets; do not commit
├── .gitignore
├── README.md
├── models/
│   ├── message.py
│   └── admin.py
├── templates/
│   ├── index.html
│   ├── about.html
│   ├── skills.html
│   ├── projects.html
│   ├── project_detail.html
│   ├── contact.html
│   ├── admin_login.html
│   └── admin.html
└── static/
    ├── css/
    ├── js/
    ├── images/
    └── Akash_Sharma_Resume.pdf
```

## Security Notes

- Keep `.env` out of Git by using `.gitignore`.
- Configure separate database URLs for local development and production.
- Use a strong, unique Flask `SECRET_KEY` in production.
- Store admin passwords as secure hashes; never place passwords in HTML or JavaScript.
- Protect admin routes with server-side authentication.
- Validate contact-form input and handle database errors without displaying sensitive exception details to visitors.
- Do not commit private keys, database credentials, or personal information submitted through the contact form.

## About Me

I'm Akash Sharma, a B.Com graduate from Jiwaji University, Gwalior, building practical skills in **Data Science, Machine Learning, Deep Learning, and Generative AI** through hands-on practice and projects.

I'm interested in entry-level opportunities and internships related to AI/ML, Data Science, and Generative AI, and I'm always keen to learn from people building useful technology.

## Connect With Me

Replace the placeholders below with your real profile links:

- **Portfolio:** Add your deployed portfolio URL
- **LinkedIn:** https://www.linkedin.com/in/akash-sharma8017/
- **GitHub:** https://github.com/Akash-sharma07/
- **Email:** akash8017sharma@gmail.com
---

<p align="center">
  Built with Python, Flask, MySQL, and a lot of learning.
</p>
