from __future__ import annotations

import hmac
import os
import re
import secrets
from functools import wraps
from pathlib import Path
from typing import Callable, TypeVar

from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from sqlalchemy.engine import URL, make_url
from sqlalchemy.exc import ArgumentError, SQLAlchemyError
from werkzeug.security import generate_password_hash

from models import db
from models.admin import Admin
from models.message import Message


ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env")


def get_database_url() -> URL:
    """Load and normalize a MySQL URL for SQLAlchemy's PyMySQL driver."""
    database_url = os.getenv("DATABASE_URL", "").strip()
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is required. Set it to a MySQL connection URL in .env "
            "or in the deployment environment."
        )

    try:
        parsed_url = make_url(database_url)
    except ArgumentError:
        raise RuntimeError("DATABASE_URL must be a valid MySQL connection URL.") from None

    if parsed_url.get_backend_name() != "mysql":
        raise RuntimeError("DATABASE_URL must point to a MySQL database.")
    if not parsed_url.host or not parsed_url.database:
        raise RuntimeError(
            "DATABASE_URL must include the MySQL host and database name."
        )

    # Accept provider URLs using mysql:// as well as explicit SQLAlchemy URLs.
    # Keep provider SSL options, and default all connections to full UTF-8.
    query = dict(parsed_url.query)
    query["charset"] = "utf8mb4"
    return parsed_url.set(drivername="mysql+pymysql", query=query)


app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv("SECRET_KEY"),
    SQLALCHEMY_DATABASE_URI=get_database_url(),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ENGINE_OPTIONS={
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "connect_args": {"connect_timeout": 10},
    },
    MAX_CONTENT_LENGTH=32 * 1024,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true",
)

if not app.config["SECRET_KEY"]:
    raise RuntimeError("Set SECRET_KEY in your local .env file before starting the app.")

try:
    db.init_app(app)
except (ImportError, SQLAlchemyError) as error:
    app.logger.error(
        "MySQL engine setup failed (%s). Install requirements.txt and check "
        "the database configuration.",
        type(error).__name__,
    )
    raise RuntimeError(
        "Could not configure the MySQL engine. Install requirements.txt "
        "and check DATABASE_URL."
    ) from None


def rollback_database_session() -> None:
    """Clear a failed transaction without surfacing a second database error."""
    try:
        db.session.rollback()
    except (ImportError, SQLAlchemyError) as error:
        app.logger.error(
            "MySQL transaction rollback failed (%s).", type(error).__name__
        )


PROJECT_SLUGS = {
    "ai-admissions-chatbot",
    "flight-database-analysis",
    "recommendify",
}
PURPOSE_OPTIONS = (
    "Job Opportunity",
    "Internship Opportunity",
    "Collaboration",
    "Feedback / Advice",
    "Project Discussion",
    "Other",
)
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
F = TypeVar("F", bound=Callable)


def csrf_token() -> str:
    """Return a session-bound token used by the small HTML forms."""
    token = session.get("_csrf_token")
    if token is None:
        token = secrets.token_urlsafe(32)
        session["_csrf_token"] = token
    return token


def valid_csrf_token(candidate: str | None) -> bool:
    expected = session.get("_csrf_token", "")
    return bool(candidate and expected and hmac.compare_digest(candidate, expected))


def admin_required(view: F) -> F:
    """Require an active admin account for a dashboard route."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        admin_id = session.get("admin_id")
        if not admin_id or db.session.get(Admin, admin_id) is None:
            session.pop("admin_id", None)
            flash("Please sign in to view the private inbox.", "info")
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)

    return wrapped  # type: ignore[return-value]


@app.context_processor
def inject_template_helpers():
    return {
        "csrf_token": csrf_token,
        "resume_available": (ROOT_DIR / "static" / "Akash_Sharma_Resume.pdf").is_file(),
        "profile_image_available": (ROOT_DIR / "static" / "images" / "profile.jpeg").is_file(),
    }


@app.after_request
def prevent_private_page_caching(response):
    if request.path.startswith("/admin"):
        response.headers["Cache-Control"] = "no-store, max-age=0"
        response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def home():
    return render_template("index.html", active_page="home")


@app.route("/about")
def about():
    return render_template("about.html", active_page="about")


@app.route("/skills")
def skills():
    return render_template("skills.html", active_page="skills")


@app.route("/projects")
def projects():
    return render_template("projects.html", active_page="projects")


@app.route("/projects/<slug>")
def project_detail(slug: str):
    if slug not in PROJECT_SLUGS:
        abort(404)
    return render_template("project_detail.html", active_page="projects", slug=slug)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        if not valid_csrf_token(request.form.get("csrf_token")):
            flash("That form session has expired. Please try again.", "error")
            return redirect(url_for("contact"))

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        purpose = request.form.get("purpose", "").strip()
        message_text = request.form.get("message", "").strip()
        problems = []

        if not name or len(name) > 100:
            problems.append("Enter your name (up to 100 characters).")
        if not email or len(email) > 254 or not EMAIL_PATTERN.fullmatch(email):
            problems.append("Enter a valid email address.")
        if purpose not in PURPOSE_OPTIONS:
            problems.append("Choose one of the listed message purposes.")
        if len(message_text) < 10 or len(message_text) > 5000:
            problems.append("Your message must be between 10 and 5,000 characters.")

        if problems:
            for problem in problems:
                flash(problem, "error")
            return render_template(
                "contact.html",
                active_page="contact",
                purpose_options=PURPOSE_OPTIONS,
                form_values=request.form,
            ), 400

        try:
            db.session.add(
                Message(name=name, email=email, purpose=purpose, message=message_text)
            )
            db.session.commit()
        except SQLAlchemyError as error:
            rollback_database_session()
            app.logger.error(
                "Contact message could not be saved to MySQL (%s).",
                type(error).__name__,
            )
            flash(
                "Your message could not be saved right now. Please try again shortly.",
                "error",
            )
            return redirect(url_for("contact"))

        flash("Thanks for reaching out. Your message has been sent.", "success")
        return redirect(url_for("contact"))

    return render_template(
        "contact.html", active_page="contact", purpose_options=PURPOSE_OPTIONS
    )


@app.route("/resume")
def resume():
    resume_path = ROOT_DIR / "static" / "Akash_Sharma_Resume.pdf"
    if not resume_path.is_file():
        flash(
            "The resume PDF has not been added yet. Place it at static/Akash_Sharma_Resume.pdf.",
            "info",
        )
        return redirect(url_for("home"))

    from flask import send_from_directory

    return send_from_directory(
        resume_path.parent,
        resume_path.name,
        as_attachment=True,
        download_name="Akash_Sharma_Resume.pdf",
    )


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_id") and db.session.get(Admin, session["admin_id"]):
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        if not valid_csrf_token(request.form.get("csrf_token")):
            flash("That sign-in form has expired. Please try again.", "error")
            return redirect(url_for("admin_login"))

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session.clear()
            session["admin_id"] = admin.id
            csrf_token()
            return redirect(url_for("admin_dashboard"))

        flash("Sign-in failed. Check your credentials and try again.", "error")

    return render_template("admin_login.html", active_page="admin")


@app.route("/admin")
@admin_required
def admin_dashboard():
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template("admin.html", active_page="admin", messages=messages)


@app.route("/admin/logout", methods=["POST"])
@admin_required
def admin_logout():
    if not valid_csrf_token(request.form.get("csrf_token")):
        flash("That sign-out form has expired. Please try again.", "error")
        return redirect(url_for("admin_dashboard"))
    session.clear()
    flash("You have been signed out.", "success")
    return redirect(url_for("admin_login"))


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html", active_page=""), 404


@app.errorhandler(500)
def server_error(_error):
    rollback_database_session()
    return render_template("500.html", active_page=""), 500


def initialize_database() -> None:
    """Create the two application tables and an initial admin when configured."""
    username = os.getenv("ADMIN_USERNAME", "").strip()
    password = os.getenv("ADMIN_PASSWORD", "")
    if bool(username) != bool(password):
        raise RuntimeError(
            "Set both ADMIN_USERNAME and ADMIN_PASSWORD in .env, or leave both empty."
        )
    if password and len(password) < 14:
        raise RuntimeError("ADMIN_PASSWORD must be at least 14 characters long.")

    with app.app_context():
        try:
            db.create_all()
            if username and not Admin.query.filter_by(username=username).first():
                db.session.add(
                    Admin(
                        username=username,
                        password_hash=generate_password_hash(password),
                    )
                )
                db.session.commit()
        except (ImportError, SQLAlchemyError) as error:
            rollback_database_session()
            app.logger.error(
                "MySQL initialization failed (%s). Check DATABASE_URL, "
                "database availability, and installed requirements.",
                type(error).__name__,
            )
            raise RuntimeError(
                "Could not initialize MySQL. Check DATABASE_URL, confirm the "
                "database is reachable, and install requirements.txt."
            ) from None


initialize_database()


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
