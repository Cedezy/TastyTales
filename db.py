from app import app, db  # import your Flask app and db

# Use application context
with app.app_context():
    db.drop_all()   # drop all tables
    db.create_all() # recreate tables with updated columns
    print("Database reset successfully!")
