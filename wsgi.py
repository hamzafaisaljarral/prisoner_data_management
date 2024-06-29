from app import create_app
import os

config_name = os.getenv('FLASK_CONFIG', 'development')
app = create_app(config_name)

# This conditional statement is typically used to run the app with Gunicorn
if __name__ == '__main__':
    app.run()
