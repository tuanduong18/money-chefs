from app import create_app
from init_db import create_tables

app = create_app()

if __name__ == '__main__':
    app.run()
