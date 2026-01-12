from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time

# ──────────────────────────────────────────────────────────────
# 1. まずは master データベースに接続し、test_db がなければ作成（autocommit モード）
# ──────────────────────────────────────────────────────────────

driver = "ODBC Driver 18 for SQL Server"
DRIVER_ENC = quote_plus(driver)

USER     = "sa"
PASSWORD = quote_plus("Pass@word")
HOST     = os.getenv("DB_HOST", "localhost")
PORT     = 1433

DB_NAME = "test_db"

MASTER_URL = (
    f"mssql+pyodbc://{USER}:{PASSWORD}@{HOST}:{PORT}/master"
    f"?driver={DRIVER_ENC}&Encrypt=no&TrustServerCertificate=yes"
)
master_engine = create_engine(MASTER_URL, pool_pre_ping=True)

# SQL Server が起動するまで待機
for i in range(30):
    try:
        with master_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        break
    except:
        time.sleep(1)
else:
    raise RuntimeError("SQL Server に接続できませんでした。")

# autocommit モードで CREATE DATABASE を実行
with master_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
    conn.execute(
        text(f"""
            IF NOT EXISTS (
                SELECT name FROM sys.databases WHERE name = N'{DB_NAME}'
            )
            CREATE DATABASE [{DB_NAME}];
        """)
    )
    # CREATE DATABASE は autocommit なので明示コミット不要

# ──────────────────────────────────────────────────────────────
# 2. test_db に接続してテーブル定義を作成する
# ──────────────────────────────────────────────────────────────

DB_URL = (
    f"mssql+pyodbc://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
    f"?driver={DRIVER_ENC}&Encrypt=no&TrustServerCertificate=yes"
)
engine = create_engine(DB_URL, pool_pre_ping=True, fast_executemany=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)
