import os
from typing import Any, Callable, Optional

import sqlalchemy
from sqlalchemy.orm import Session, sessionmaker


class CockroachDBClient:
    ENV_URL = "COCKROACH_DB_URL"

    def __init__(self, url: Optional[str] = None):
        # self.url = url or os.environ[self.ENV_URL]
        self.db_name = os.environ["DB_NAME"]
        self.db_user = os.environ["DB_USER"]
        self.db_pass = os.environ["DB_PASS"]
        self.db_host = os.environ["DB_HOST"]
        self.db_port = os.environ["DB_PORT"]
        self.ssl_mode = "require"
        self.ssl_cert = os.environ["SSL_CERT_PATH"]
        self.engine = sqlalchemy.create_engine(
            f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}?sslmode={self.ssl_mode}&sslrootcert={self.ssl_cert}"
        )

    def get_session_maker(self):
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def query(self, fn: Callable[[Session, ...], Any], **kwargs):
        # Instead of using run_transaction, directly execute the provided function
        session = self.get_session_maker()()
        try:
            result = fn(session, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
