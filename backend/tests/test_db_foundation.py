import os
import unittest
from unittest.mock import patch

from sqlalchemy.orm import Session, sessionmaker

from backend.app.core.config import get_settings
from backend.app.db.session import build_engine, get_db


class DatabaseFoundationTestCase(unittest.TestCase):
    def tearDown(self) -> None:
        get_settings.cache_clear()

    def test_settings_reads_database_url_from_environment(self) -> None:
        with patch.dict(os.environ, {"DATABASE_URL": "sqlite+pysqlite:///:memory:"}, clear=False):
            get_settings.cache_clear()

            settings = get_settings()

        self.assertEqual(settings.database_url, "sqlite+pysqlite:///:memory:")

    def test_get_db_yields_session_from_configured_sessionmaker(self) -> None:
        engine = build_engine("sqlite+pysqlite:///:memory:")
        testing_session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, class_=Session)

        with patch("backend.app.db.session.create_session", side_effect=testing_session_local):
            session_generator = get_db()
            session = next(session_generator)

            self.assertIsInstance(session, Session)
            self.assertEqual(session.bind.url.render_as_string(hide_password=False), "sqlite+pysqlite:///:memory:")

            session_generator.close()


if __name__ == "__main__":
    unittest.main()
