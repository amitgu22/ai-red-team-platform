import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
URL=os.getenv("DATABASE_URL","postgresql+psycopg://redteam:redteam@localhost:5432/redteam")
engine=create_engine(URL,pool_pre_ping=True)
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)
class Base(DeclarativeBase): pass
def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()
def init_db():
    from app import models
    Base.metadata.create_all(bind=engine)
    # POC migration for Phase 2.1 when reusing an existing Phase 2 volume.
    with engine.begin() as conn:
        conn.exec_driver_sql("ALTER TABLE test_runs ADD COLUMN IF NOT EXISTS attempt INTEGER NOT NULL DEFAULT 1")
    # Phase 4 risk/governance tables are created by metadata above.
    from app.seed import seed
    db=SessionLocal()
    try: seed(db)
    finally: db.close()
