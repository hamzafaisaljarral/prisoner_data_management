import os

from dotenv import load_dotenv
load_dotenv()  # This will load environment variables from .env file

from flask_migrate import Migrate
from app import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'development')
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)
