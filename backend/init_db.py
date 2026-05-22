import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings
from app.database.base import Base
import app.models as models  # noqa: F401
from app.utils.security import hash_password


def try_create_engine(url: str):
    try:
        engine = create_engine(url, future=True)
        # try connect
        conn = engine.connect()
        conn.close()
        return engine, url
    except Exception:
        return None, None


def main():
    os.makedirs(os.path.dirname(settings.upload_dir), exist_ok=True)
    os.makedirs(os.path.dirname(settings.vector_dir), exist_ok=True)

    engine, used_url = try_create_engine(settings.database_url)
    if engine is None:
        if settings.allow_sqlite_fallback:
            sqlite_path = os.path.abspath(os.path.join(os.getcwd(), "backend", "storage", "dev.db"))
            os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
            sqlite_url = f"sqlite:///{sqlite_path}"
            print(f"Could not connect to configured DATABASE_URL. Falling back to SQLite at {sqlite_path}")
            engine = create_engine(sqlite_url, future=True)
            used_url = sqlite_url
        else:
            raise RuntimeError("Could not connect to MySQL using DATABASE_URL. Set ALLOW_SQLITE_FALLBACK=true only for local testing.")

    print(f"Using database: {used_url}")

    # create tables
    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        # create roles
        from app.models.role import Role
        from app.models.user import User

        admin_role = db.query(Role).filter(Role.name == "Admin").first()
        if not admin_role:
            admin_role = Role(name="Admin")
            db.add(admin_role)

        user_role = db.query(Role).filter(Role.name == "User").first()
        if not user_role:
            user_role = Role(name="User")
            db.add(user_role)

        db.commit()

        # create default admin user
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin:
            admin = User(email="admin@example.com", password_hash=hash_password("admin123"), role_id=admin_role.id)
            db.add(admin)
            db.commit()
            print("Created default admin user: admin@example.com / admin123")
        else:
            print("Admin user already exists")

        # create default normal user
        normal_user = db.query(User).filter(User.email == "user@example.com").first()
        if not normal_user:
            normal_user = User(
                email="user@example.com",
                password_hash=hash_password("user123"),
                role_id=user_role.id,
            )
            db.add(normal_user)
            db.commit()
            print("Created default user: user@example.com / user123")
        else:
            print("Normal user already exists")

    except Exception as exc:
        print("Error seeding data:", exc)
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
