"""
Database Initialization Script
Creates all necessary tables for secure file sharing
Run this script before starting the backend
"""

from sqlalchemy import create_engine, inspect
from database.database import DATABASE_URL
from database.models import Base


def init_database():
    """Initialize database and create all tables"""

    print("=" * 60)
    print("DATABASE INITIALIZATION")
    print("=" * 60)

    try:
        # Create engine
        engine = create_engine(DATABASE_URL)

        # Get inspector
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        print(f"\nExisting tables: {existing_tables}")

        # Create all tables
        print("\nCreating tables...")
        Base.metadata.create_all(bind=engine)

        # Verify tables were created
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        print(f"\nTables after initialization: {tables}")

        # List new tables created
        new_tables = set(tables) - set(existing_tables)

        if new_tables:
            print(f"\nNew tables created: {new_tables}")
        else:
            print("\nNo new tables created (all already exist)")

        print("\n✓ Database initialization complete!")

        # Print table schemas
        print("\n" + "=" * 60)
        print("TABLE SCHEMAS")
        print("=" * 60)

        for table_name in tables:
            print(f"\n{table_name}:")
            columns = inspector.get_columns(table_name)
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")

    except Exception as e:
        print(f"\n✗ Database initialization failed: {str(e)}")
        raise


if __name__ == "__main__":
    init_database()
