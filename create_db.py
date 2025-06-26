from models import Base, engine

# This will create the table in usage.db
Base.metadata.create_all(bind=engine)
print("Database and table created!")