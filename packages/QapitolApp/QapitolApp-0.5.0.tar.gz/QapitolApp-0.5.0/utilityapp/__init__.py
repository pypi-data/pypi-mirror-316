from flask import Flask

app = Flask(__name__)


# Import the views (routes)
from . import app as app_module

# You can also configure your app here if needed
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ARCHIVE_FOLDER'] = 'archive'
app.config['LOG_FOLDER'] = 'logs'

# Ensure the app is properly initialized
def create_app():
    return app