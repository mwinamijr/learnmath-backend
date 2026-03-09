from sqlalchemy import text
from app.database import engine


def test_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("Database connection successfully!")
    except Exception as e:
        print(f"Database connection failed: {e}")


if __name__ == "__main__":
    test_connection()
