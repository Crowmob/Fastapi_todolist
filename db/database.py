from sqlalchemy.orm import sessionmaker
from project.models import *

DATABASE_URL = "postgresql://postgres:valera10z@localhost:5432/tasks"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# Close session
def disconnect_db():
    session.close()
