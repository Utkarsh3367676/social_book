from sqlalchemy import create_engine, text

# Replace these with your actual database credentials
DB_URL = "postgresql://admin:user@localhost:5432/social_book_db"

engine = create_engine(DB_URL)

# def get_uploaded_files(user_id):
#     with engine.connect() as connection:
#         # Add a WHERE clause to filter files by user ID
#         query = text("SELECT * FROM accounts_uploadedfile WHERE user_id = :user_id;")  # Replace with your actual table and column names
#         result = connection.execute(query, {'user_id': user_id})
#         return [{column: row[column] for column in row.keys()} for row in result]
def get_uploaded_files(user_id):
    with engine.connect() as connection:
        query = text("SELECT * FROM accounts_uploadedfile WHERE user_id = :user_id;")
        result = connection.execute(query, {'user_id': user_id})
        
        # Convert rows to dictionaries using mappings() method
        return [dict(row) for row in result.mappings()]
