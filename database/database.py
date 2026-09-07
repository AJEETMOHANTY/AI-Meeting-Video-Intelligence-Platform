# Create Connection -> Create Engine -> Create Session

# Step 1: Load .env
# Step 2: Connect to PostgreSQL
# Step 3: Create Session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# Read DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Create PostgreSQL Engine
engine = create_engine(DATABASE_URL)

# Create Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ===== DB Connection Check =====
from sqlalchemy import text

try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("✅ Connected to PostgreSQL Successfully!")
except Exception as e:
    print(f"❌ Connection Failed:\n{e}")

# ==========================
# Concept Understanding: Engine, Session, Connection, PostgreSQL
# ==========================

# Engine is set up first;
# Session is created from the Engine;
# When the Session needs to talk to PostgreSQL,
# The Engine manages the Connection.

# Engine → Contains the database configuration, such as which database we use, its location, username, password, etc., and manages connections.
# Session → Provides an interface for Python to perform database operations/queries.
# Connection → Acts as the actual communication channel that carries database operations between Python and PostgreSQL.
# PostgreSQL → Receives and executes the query, then returns the result back through the connection.
