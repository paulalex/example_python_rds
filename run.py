"""
Run the python application for local development - Not for production use
"""
from project import create_app
from project import create_db

app = create_app()
create_db()
app.run(host='0.0.0.0', port=5000, debug=True)
