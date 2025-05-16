from flask_cors import CORS
from app import create_app
from init_db import create_tables

app = create_app()

CORS(app)
create_tables()

if __name__ == '__main__':
    app.run(debug = True)
