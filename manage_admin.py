"""Safely inspect and manage the first portfolio admin on Aiven MySQL.

Run this only from the Render service shell or with an Aiven URL entered via
the hidden prompt. Passwords are prompted interactively and never accepted as
command-line arguments.
"""

from __future__ import annotations

import argparse
import getpass
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import inspect, select
from sqlalchemy.engine import URL, make_url
from sqlalchemy.exc import ArgumentError, IntegrityError, SQLAlchemyError
from werkzeug.security import generate_password_hash


ROOT_DIR = Path(__file__).resolve().parent
MIN_PASSWORD_LENGTH = 14


class AdminToolError(Exception):
    """An expected, safe-to-display CLI error."""


def configure_aiven_database(prompt_database_url: bool) -> URL:
    """Require a remote Aiven host and CA-verified TLS before any DB access."""
    load_dotenv(ROOT_DIR / ".env")

    if prompt_database_url:
        entered_url = getpass.getpass("Paste the Aiven DATABASE_URL (hidden): ").strip()
        if not entered_url:
            raise AdminToolError("No database URL was entered.")
        os.environ["DATABASE_URL"] = entered_url

    raw_url = os.getenv("DATABASE_URL", "").strip()
    if not raw_url:
        raise AdminToolError("DATABASE_URL is not set in this environment.")

    try:
        parsed_url = make_url(raw_url)
    except (ArgumentError, ValueError):
        raise AdminToolError("DATABASE_URL is not a valid SQLAlchemy URL.") from None

    host = (parsed_url.host or "").lower().rstrip(".")
    if parsed_url.get_backend_name() != "mysql" or not parsed_url.database:
        raise AdminToolError("DATABASE_URL must identify a MySQL database.")
    if not host.endswith(".aivencloud.com"):
        raise AdminToolError(
            "Refusing to connect: this tool only permits an Aiven MySQL hostname. "
            "This prevents accidental changes to local MySQL."
        )

    query = dict(parsed_url.query)
    ca_value = query.get("ssl_ca") or os.getenv("AIVEN_CA_CERT", "").strip()
    if not ca_value:
        raise AdminToolError(
            "Aiven TLS CA is required. Add ssl_ca to DATABASE_URL or set "
            "AIVEN_CA_CERT to the mounted Aiven CA file path."
        )

    ca_path = Path(ca_value).expanduser()
    if not ca_path.is_absolute():
        ca_path = ROOT_DIR / ca_path
    ca_path = ca_path.resolve()
    if not ca_path.is_file():
        raise AdminToolError(
            "The configured Aiven CA certificate file is missing or unreadable."
        )

    # Aiven service URIs may contain ssl-mode=REQUIRED for generic clients.
    # PyMySQL's SQLAlchemy dialect uses ssl_ca; use it for CA-verified TLS.
    query.pop("ssl-mode", None)
    query.pop("ssl_mode", None)
    query["ssl_ca"] = str(ca_path)
    query["charset"] = "utf8mb4"
    normalized_url = parsed_url.set(drivername="mysql+pymysql", query=query)

    # This is process-local only. The URL is never printed or put in argv.
    os.environ["DATABASE_URL"] = normalized_url.render_as_string(hide_password=False)
    return normalized_url


def load_app_without_startup_seeding():
    """Import the real app/models without create_all or env-based admin seeding."""
    os.environ["ADMIN_USERNAME"] = ""
    os.environ["ADMIN_PASSWORD"] = ""

    from models import db

    original_create_all = db.create_all
    db.create_all = lambda *args, **kwargs: None
    try:
        import app as portfolio_app
    finally:
        db.create_all = original_create_all

    return portfolio_app.app, db, portfolio_app.Admin


def read_admins(app, db, Admin):
    """Return table existence and only IDs/usernames, never password hashes."""
    with app.app_context():
        try:
            with db.engine.connect() as connection:
                table_exists = inspect(connection).has_table(Admin.__tablename__)
            if not table_exists:
                return False, []
            rows = db.session.execute(
                select(Admin.id, Admin.username).order_by(Admin.id)
            ).all()
            return True, rows
        except SQLAlchemyError as error:
            db.session.rollback()
            raise AdminToolError(
                "Aiven database inspection failed "
                f"({type(error).__name__}). Check Render/Aiven networking and TLS."
            ) from None


def confirm_target(host: str) -> None:
    print(f"Target Aiven MySQL host: {host}")
    if input("Type this host exactly to authorize the change: ").strip() != host:
        raise AdminToolError("Target confirmation did not match; no changes made.")


def prompt_password() -> str:
    password = getpass.getpass("New admin password (input hidden): ")
    repeated = getpass.getpass("Repeat new admin password: ")
    if password != repeated:
        raise AdminToolError("The passwords did not match; no changes made.")
    if len(password) < MIN_PASSWORD_LENGTH:
        raise AdminToolError(
            f"Use a password with at least {MIN_PASSWORD_LENGTH} characters."
        )
    return password


def command_status(app, db, Admin, target: URL) -> int:
    exists, rows = read_admins(app, db, Admin)
    print(f"Connected to Aiven MySQL: {target.host}:{target.port}/{target.database}")
    print("TLS: Aiven CA certificate configured and present")
    print(f"Admin table: {'exists' if exists else 'missing'}")
    if exists and rows:
        print(f"Admin accounts found: {len(rows)}")
        for admin_id, username in rows:
            print(f"  id={admin_id} username={username}")
    elif exists:
        print("Admin accounts found: 0")
    return 0 if exists else 2


def command_create(app, db, Admin, target: URL) -> int:
    exists, rows = read_admins(app, db, Admin)
    if rows:
        print("An admin account already exists; no account or password was changed.")
        for admin_id, username in rows:
            print(f"  id={admin_id} username={username}")
        print("Use the reset command for an existing username.")
        return 2

    confirm_target(target.host or "")
    username = input("Initial admin username: ").strip()
    if not username or len(username) > 80:
        raise AdminToolError("Username must contain 1 to 80 characters.")
    password = prompt_password()

    with app.app_context():
        try:
            if not exists:
                # Models are imported before this command; create only missing tables.
                db.create_all()
            if Admin.query.filter_by(username=username).first():
                db.session.rollback()
                print("That username already exists; no password was changed.")
                return 2
            db.session.add(
                Admin(
                    username=username,
                    password_hash=generate_password_hash(password),
                )
            )
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise AdminToolError(
                "The account could not be created, likely because another admin "
                "was added concurrently. Run the status command."
            ) from None
        except SQLAlchemyError as error:
            db.session.rollback()
            raise AdminToolError(
                f"Admin creation failed ({type(error).__name__}); no plaintext "
                "password was stored."
            ) from None
        finally:
            password = ""

    print(f"Created initial admin account '{username}' with a Werkzeug password hash.")
    return 0


def command_reset(app, db, Admin, target: URL, username: str) -> int:
    username = username.strip()
    if not username:
        raise AdminToolError("Specify the existing admin username to reset.")

    with app.app_context():
        try:
            admin = Admin.query.filter_by(username=username).first()
        except SQLAlchemyError as error:
            db.session.rollback()
            raise AdminToolError(
                f"Admin lookup failed ({type(error).__name__})."
            ) from None
        if admin is None:
            print("No account with that username exists; no account was created.")
            return 2

        confirm_target(target.host or "")
        password = prompt_password()
        try:
            admin.password_hash = generate_password_hash(password)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            raise AdminToolError(
                f"Password reset failed ({type(error).__name__})."
            ) from None
        finally:
            password = ""

    print(f"Reset the password for existing admin account '{username}'.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--prompt-database-url",
        action="store_true",
        help="read the Aiven URL through a hidden prompt instead of the environment",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("status", help="test Aiven connectivity and list usernames")
    subparsers.add_parser("create", help="create the first admin only if none exist")
    reset_parser = subparsers.add_parser("reset", help="reset an existing admin password")
    reset_parser.add_argument("username")
    args = parser.parse_args()

    try:
        target = configure_aiven_database(args.prompt_database_url)
        app, db, Admin = load_app_without_startup_seeding()
        if args.command == "status":
            return command_status(app, db, Admin, target)
        if args.command == "create":
            return command_create(app, db, Admin, target)
        return command_reset(app, db, Admin, target, args.username)
    except AdminToolError as error:
        print(f"Admin tool: {error}", file=sys.stderr)
        return 1
    except (ImportError, SQLAlchemyError) as error:
        print(
            f"Admin tool could not load the database driver ({type(error).__name__}). "
            "Install requirements.txt and check the Render service configuration.",
            file=sys.stderr,
        )
        return 1
    except RuntimeError as error:
        print(f"Admin tool could not initialize the Flask app: {error}", file=sys.stderr)
        return 1
    except (EOFError, KeyboardInterrupt):
        print("Cancelled; no changes made.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
