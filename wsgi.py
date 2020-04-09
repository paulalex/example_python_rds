"""
Run the python application in production
"""
from project import create_app
from project import create_db

app = create_app()
create_db()

if __name__ == "__main__":
    app.run()
