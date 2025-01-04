from sqlalchemy import create_engine, text

# Replace these with your actual database credentials
DB_URL = "postgresql://admin:admin@localhost:5432/social_book_db"

engine = create_engine(DB_URL)

def get_uploaded_files():
    with engine.connect() as connection:
        query = text("SELECT * FROM uploaded_files;")  # Replace with your actual table name
        result = connection.execute(query)
        return [dict(row) for row in result]
